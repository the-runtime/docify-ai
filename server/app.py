from fastapi import FastAPI, status, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import google_auth_oauthlib.flow

import hashlib
import os
import requests

app = FastAPI()
# @app.middleware("http")
# def get_user_info(req: Request, call_next):
#     user_info = req.session.get("user_info")
#     # if not user_info:
#     #     return HTMLResponse("Not authenticated <a href='/google_auth'>Login</a>")
#     call_next(req, user_info)
#     return HTMLResponse("From middleware")

origins = [
    "http://127.0.0.1:3000"
]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.add_middleware(SessionMiddleware, secret_key="secret_keY")  # take from config (env)
# app.add_middleware()
# middleware to get userinfo

# security = OpenIdConnect("/api/auth/google")

# for google oauth service
json_file = "/home/tabish/Documents/Projects/docify-ai/client_secret_1015116338006-oa6d1dgtniq8oj07amhf9l1qn2s2qh0m.apps.googleusercontent.com.json"
scopes = ['openid', 'https://www.googleapis.com/auth/userinfo.profile']

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(json_file, scopes=scopes)
flow.redirect_uri = "http://127.0.0.1:8080/auth/google/callback"


def get_user_info(req: Request):
    user_info = req.session.get("user")
    # if not user_info:
    #     return HTMLResponse("Not authenticated <a href='/google_auth'>Login</a>")
    return user_info


@app.get("/")
def root_test():
    return "Hello world"


@app.get("/auth/google")
def google_auth(req: Request):
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    authorization_url, res_state = flow.authorization_url(
        state=state,
        # access_type='offline',
        include_granted_scopes='true'
    )
    req.session["state"] = state

    return RedirectResponse(authorization_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/auth/google/callback")
async def google_auth_callback(req: Request):
    query_params = req.query_params
    openid_state = query_params.get("state")
    openid_code = query_params.get("code")
    # print("code: ", openid_code)
    if req.session.get("state") != openid_state:
        # use logger to get log of fraud login attempt
        return HTMLResponse("Error while verifying")

    token = flow.fetch_token(code=openid_code)
    # print(token)
    get_usr_url = "https://www.googleapis.com/oauth2/v2/userinfo?access_token=" + token.get("access_token")
    user_info = requests.get(url=get_usr_url)
    # print(user_info.text)
    if user_info.status_code == status.HTTP_200_OK:
        req.session["user"] = user_info.json()
        return RedirectResponse("http://127.0.0.1:3000/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    else:
        print("error find user")
        return HTMLResponse("Error finding user try again after some time")


@app.get("/secure")
def access_secure(req: Request, user_info: dict = Depends(get_user_info)):
    # print(user_info)
    if user_info is None:
        return
    else:
        return HTMLResponse("Success :" + str(user_info))


@app.get("/checkauth")
def check_auth(user_info: dict = Depends(get_user_info)):
    if user_info is None:
        ret_resp = {"is_authenticated": False}
    else:
        ret_resp = {"is_authenticated": True}

    return JSONResponse(ret_resp)
