import asyncio
from pathlib import Path
import sys
from docifyai.core import model
from docifyai.services import get_repo
from docifyai.core import logger
from docifyai.utils import utils
from docifyai.core.preprocess import RepoParseFunc as repo_parse
from docifyai.langaugeSupport import get_lang_support
from docifyai.document.aiDoc import Aidoc
from docifyai.config.config import enVar

logger = logger.Logger(__name__)


async def docify_run() -> None:
    logger.info("Welcome to docify-ai prototype testing")
    # url = sys.argv[1]
    url = "https://github.com/eli64s/Readme-ai"
    branch = "main"
    working_folder = "readmeai"
    # url = "https://github.com/the-runtime/serverDowndrive"

    repo_info = get_repo.get_github_repo_metadata(url)
    logger.info(f"Repo info {repo_info}")

    # load environment variables
    env_var = enVar()
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
        logger.info(f"Document Created: {doc_name}")
        # logger.info(f"Code summaries returned:\n{code_details[:5]}")

    except Exception as excinfo:
        logger.error(
            f"Exception: {excinfo}\n"
        )
    finally:
        await llm.close()

    logger.info("Docify-ai execution completes.")


def main() -> None:
    asyncio.run(docify_run())


if __name__ == "__main__":
    main()
