from fastapi import FastAPI, status, Depends, Request, staticfiles, Response
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import google_auth_oauthlib.flow
import hashlib
import os
import requests
import razorpay

from redis import Redis
from rq import Queue

from fastapi.templating import Jinja2Templates

from server.database import database
from server.model import routeResponse, models
from server.controller import blobcontroller
from server.config import config
from docifyai.core import logger
from server.workers import job
from server.model.routeRequest import PaymentCapturedPayload

logger = logger.Logger(__name__)

env_var = config.enVar()
"""Some connection strings"""
azure_blob_strings = [
    env_var.azure_blob_key,
    env_var.blob_container_name
]
redis_conn = Redis.from_url(env_var.redis_url)
job_que = Queue(name=env_var.redis_queue_name, connection=redis_conn, default_timeout=60*20)

app = FastAPI()
db = database.Database(env_var.postgres_url)

# @app.middleware("http")
# def get_user_info(req: Request, call_next):
#     user_info = req.session.get("user_info")
#     # if not user_info:
#     #     return HTMLResponse("Not authenticated <a href='/google_auth'>Login</a>")
#     call_next(req, user_info)
#     return HTMLResponse("From middleware")

# use origin of the react app
# origins = [
#     "http://127.0.0.1:3000"
# ]
# app.add_middleware(CORSMiddleware,
#                    allow_origins=origins,
#                    allow_credentials=True,
#                    allow_methods=["*"],
#                    allow_headers=["*"],
#                    )

app.add_middleware(SessionMiddleware, secret_key=env_var.server_secret_key)  # take from config (env)
# app.add_middleware()
# middleware to get userinfo

# security = OpenIdConnect("/api/auth/google")

# for Google oauth service
json_file = env_var.google_json_file
scopes = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(json_file, scopes=scopes)
flow.redirect_uri = env_var.google_redirect_uri

def get_user_info(req: Request):
    user_info = req.session.get("user_id")
    # if not user_info:
    #     return HTMLResponse("Not authenticated <a href='/google_auth'>Login</a>")
    return user_info


@app.get("/auth/google")
def google_auth(req: Request):
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    authorization_url, res_state = flow.authorization_url(
        state=state,
        # access_type='offline',
        # include_granted_scopes='true'
    )
    req.session["state"] = state

    return RedirectResponse(authorization_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/auth/google/callback")
async def google_auth_callback(req: Request):
    db_session = db.get_session()
    query_params = req.query_params
    openid_state = query_params.get("state")
    openid_code = query_params.get("code")
    # print("code: ", openid_code)
    if req.session.get("state") != openid_state:
        # use logger to get log of fraud login attempt
        return HTMLResponse("Error while verifying")

    token = flow.fetch_token(code=openid_code)
    get_usr_url = "https://www.googleapis.com/oauth2/v2/userinfo?access_token=" + token.get("access_token")
    user_info_resp = requests.get(url=get_usr_url)
    if user_info_resp.status_code == status.HTTP_200_OK:
        user_info = user_info_resp.json()
        req.session["user_id"] = user_info.get("id")
        user_db = db_session.query(models.User).filter_by(id=user_info.get("id")).first()
        if user_db:
            logger.debug("user_db found don't know how")
            return RedirectResponse("/app/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        # use logic to check if user exists on database
        logger.info(user_info)
        new_user = models.User(
            id=user_info.get("id"),
            username=user_info.get("name"),
            email=user_info.get("email"),
            img_url=user_info.get("picture"),
            credits=1000,
        )
        db_session.add(new_user)
        db_session.commit()
        logger.info(f"New user named: {user_info.get('name')} added to database")
        return RedirectResponse("/app/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    else:
        logger.info("error find user")
        return HTMLResponse("Error finding user try again after some time")


# @app.get("/secure")
# def access_secure(req: Request, user_info: dict = Depends(get_user_info)):
#     # print(user_info)
#     if user_info is None:
#         return
#     else:
#         return HTMLResponse("Success :" + str(user_info))
#


@app.post("/payment/captured")
async def capture_payment(request: Request, payload: PaymentCapturedPayload):
    client = razorpay.Client(auth=("[YOUR_KEY_ID]", "[YOUR_KEY_SECRET]"))
    secret_key = env_var.server_secret_key
    client_secret_key = request.headers.get("X-Razorpay-Signature")
    request_json = await request.json()
    client.utility.verify_webhook_signature(request_json, client_secret_key, secret_key)
    if secret_key != client_secret_key:
        logger.debug("secret didn't matched")
        return
    amount = int(payload["payment"]["entity"]["base_amount"]) / 100
    credits = (amount / 20) * 1000
    db_session = db.get_session()
    user = db_session.query(models.User).filter_by(email=payload["payment"]["enitity"]["base_amount"]["email"]).first()
    if not user:
        # mail to email that it isn't registered
        return
    logger.debug("Credits is {}".format(credits))
    user.update({"credits": user.credits + credits})
    db_session.commit()
    # may mail user about the credits
    return








@app.get("/api/logout")
def delete_session(req: Request, user_info: dict = Depends(get_user_info)):
    if user_info is None:
        return JSONResponse("Not authenticated", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if "user_id" in req.session:
        del req.session['user_id']
    return RedirectResponse("/app/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# @app.get("api/delete")
# def delete_account()
@app.get("/api/checkauth")
def check_auth(user_info: dict = Depends(get_user_info)):
    if user_info is None:
        ret_resp = {"is_authenticated": False}
    else:
        ret_resp = {"is_authenticated": True}

    return JSONResponse(ret_resp)


@app.get("/api/userinfo", response_model=routeResponse.Userinfo | str)
def get_api_userinfo(user_id: str = Depends(get_user_info)):
    if user_id is None:
        return JSONResponse("Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
        # return routeResponse.ErrorClass.error.append("Error finding user")
    session = db.get_session()
    user_info_db: models.User = session.query(models.User).filter_by(id=user_id).first()
    if user_info_db:
        return routeResponse.Userinfo(
            name=user_info_db.username,
            email=user_info_db.email,
            credits=user_info_db.credits,
            imageUrl=user_info_db.img_url
        )

    return routeResponse.ErrorClass.error.append("User not in Database")


@app.get('/api/history', response_model=routeResponse.History | str)
def get_history(user_id: str = Depends(get_user_info)):
    if user_id is None:
        return JSONResponse("Not Authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    user_db = db.get_session().query(models.User).filter_by(id=user_id).first()

    if user_db:
        list_history = []
        download_history = user_db.docify_history
        for single_history in download_history:
            list_history.append(
                routeResponse.singleHistory(
                    historyId=single_history.id,
                    filename=single_history.filename.split("/")[-1],
                    fileDownloadLink=f"https://docify.tabish.tech/api/getdoc/?blob_name={single_history.filename}",
                    # need to modify it before sending (azure security)
                    generationTime=single_history.gen_time,
                )
            )
        return routeResponse.History(
            username=user_db.username,
            history=list_history
        )
    else:
        logger.error("User got to History without having account")
        return JSONResponse("Internal Server Error", status_code=401)


"""Registers the work to generate the document"""


@app.get("/api/document/")
async def generate_doc(url: str, branch: str, work_dir: str, user_id: str = Depends(get_user_info)):
    if not user_id:
        return "Not authenticated"  # also add status type for client to handle it gracefully
    logger.info("User_id is ", user_id)  # here some error is happening
    doc_job = job_que.enqueue(job.docify_job, url, branch, azure_blob_strings, user_id, work_dir)
    # return "Process started"
    return RedirectResponse("/app/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/api/get-jobs-info")
async def get_job_info(user_id: str = Depends(get_user_info)):
    """Use another redis DS to the access the jobs in progress """
    return HTMLResponse("Not implemented yet")


@app.get("/api/getdoc/")
async def get_doc_from_azure(blob_name: str, response: Response, user_id: str = Depends(get_user_info)):
    if not user_id:
        return "Not authorized"

    blob_data = blobcontroller.get_from_azure_blob(blob_name, azure_blob_strings)
    blob_iter = blob_data.chunks()
    return StreamingResponse(blob_iter, 200, media_type="application/octet-stream",
                             headers={"Content-Disposition": f"attachment; filename={blob_name}"})

    # return StreamingResponse()


"""Handle react app frontend"""

public_dir = "server/react-app"
templates = Jinja2Templates(directory=public_dir)


@app.get("/app", include_in_schema=False)
async def redirect_landing_page():
    return RedirectResponse("/app/", status_code=status.HTTP_308_PERMANENT_REDIRECT)


@app.get("/app/{path:path}", include_in_schema=False)
async def serve_react_app(req: Request, path: str):
    check_react_route = True if len(path.split(".")) == 1 else False
    if path == "index.html" or check_react_route:
        return templates.TemplateResponse("App.html", context={'request': req})
    elif not check_react_route:
        return FileResponse(f"{public_dir}/{path}")


# change this /holly-react with /
# @app.get("/holly-react")
# async def redirect_landing_page():
#     return RedirectResponse("/holly-react/", status_code=status.HTTP_308_PERMANENT_REDIRECT)


@app.get("/{path:path}", include_in_schema=False)
async def serve_landing_page(req: Request, path: str):
    check_react_route = True if len(path.split(".")) == 1 else False
    if path == "index.html" or check_react_route:
        return templates.TemplateResponse("index.html", {"request": req})
    elif not check_react_route:
        return FileResponse(f"{public_dir}/{path}")
    else:
        logger.debug("Some how react request got here")
