import asyncio
from typing import List
from pathlib import Path
from docifyai.core import model
from docifyai.services import get_repo
from docifyai.core import logger
from docifyai.utils import utils
from docifyai.core.preprocess import RepoParseFunc as repo_parse
from docifyai.langaugeSupport import get_lang_support
from docifyai.document.aiDoc import Aidoc
from docifyai.config.config import enVar
from server.database import database
from server.model import models as db_models
# import from server , have to change in future
from server.controller import blobcontroller
from server.workers import emailNotify

logger = logger.Logger(__name__)


async def docify_run(url: str, branch: str, blob_configs: List[str], user_id: str, working_folder: str) -> None:
    logger.info("Welcome to docify-ai prototype testing")

    # load environment variables
    env_var = enVar()  # use config file

    repo_info = get_repo.get_github_repo_metadata(url, env_var.github_token)
    # logger.info(f"Repo info {repo_info}")

    db = database.Database(
        env_var.postgres_url)  # use from env file
    # db_session = db.get_session()

    # user associated with the user_id
    user_info = db.Session.query(db_models.User).filter_by(id=user_id).first()

    user_name = user_info.username
    user_email = user_info.email
    logger.debug(user_info.username)

    temp_dir = get_repo.clone_repo(url, branch)
    working_path = utils.get_working_path_of_project(working_folder, Path(temp_dir))
    llm = model.OpenAIHandler(env_var)

    try:
        files = repo_parse.get_files(temp_dir)
        # first find the language name then, for now just python is used

        lang_support = get_lang_support(name="python", files=files, project_path=temp_dir)
        # dependency dict
        depend_dict = lang_support.get_depend_dict()
        # logger.info(f"Files: {files}")
        code_details_tuple = await llm.code_to_text(
            utils.get_ignore_files(),
            files,
            utils.get_implementation_prompt(),
            depend_dict
        )
        code_details = utils.change_tuple_to_dict(code_details_tuple)
        folders_details_tuple = await llm.folder_to_text(
            code_details,
            working_path,
            temp_dir,
            utils.get_folders_prompt()

        )
        folder_details = utils.change_tuple_to_dict(folders_details_tuple)
        intro_tuple = await llm.get_text_for_intro(folder_details, utils.get_intro_prompt())
        document = Aidoc(repo_info, temp_dir, code_details, folder_details, intro_tuple)
        # will use path for letting user download it
        doc_name = document.create_document()
        blobcontroller.upload_to_azure_blob(doc_name, blob_configs)
        logger.info(f"Document Created and saved to azure: {doc_name}")
        emailNotify.send_mail_to_user(is_success=True, api_key=env_var.brevo_key, user_name=user_name,
                                      user_email=user_email, file_name=doc_name)

        single_history = db_models.History(
            user_id=user_id,
            filename=doc_name,
        )

        db.Session.add(single_history)
        db.Session.commit()
        db.Session.flush()
        db.Session.close()
        # logger.info(f"Code summaries returned:\n{code_details[:5]}")

    except Exception as excinfo:
        emailNotify.send_mail_to_user(is_success=False, api_key=env_var.brevo_key, user_name=user_name,
                                      user_email=user_email)
        logger.error(
            f"Exception: {excinfo}\n"
        )
    finally:
        await llm.close()

    logger.info("Docify-ai execution completes.")


def docify_job(url: str, branch: str, blob_configs, user_id, work_dir) -> None:
    asyncio.run(docify_run(url, branch, blob_configs, user_id, work_dir))
