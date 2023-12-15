import asyncio
from pathlib import Path
import sys
from docifyai.core import model_v2 as model
from docifyai.services import get_repo
from docifyai.core import logger
from docifyai.utils import utils
from docifyai.core.preprocess import RepoParseFunc as repo_parse
from docifyai.langaugeSupport import get_lang_support
from docifyai.document.aiDoc_v2 import Aidoc
from docifyai.config.config import enVar

# for testing
import shutil

logger = logger.Logger(__name__)


async def docify_run() -> None:
    logger.info("Welcome to docify-ai prototype testing")
    # url = sys.argv[1]
    url = "https://github.com/the-runtime/serverDowndrive"
    branch = "main"
    working_folder = "."
    # url = "https://github.com/the-runtime/serverDowndrive"



    # load environment variables
    env_var = enVar()
    repo_info = get_repo.get_github_repo_metadata(url, env_var.github_token)
    logger.info(f"Repo info {repo_info}")
    temp_dir = get_repo.clone_repo(url, branch)
    # working_path = utils.get_working_path_of_project(working_folder, Path(temp_dir))
    llm = model.OpenAIHandler(env_var, temp_dir)

    try:
        files = repo_parse.get_files(temp_dir)
        # first find the language name then, for now just python is used

        lang_support = get_lang_support(name="python", files=files, project_path=temp_dir)
        # dependency dict
        depend_dict = lang_support.get_depend_dict()
        # logger.info(f"Files: {files}")
        code_details_tuple = await llm.read_code(
            utils.get_ignore_files(),
            files,
            utils.get_prompt_for_code_info(),
            depend_dict
        )
        code_details = utils.change_tuple_to_dict(code_details_tuple)
        init_overview = await llm.get_initial_overview_of_project(code_details, utils.get_prompt_for_init_info())

        chapter_names = await llm.get_chapters_name(init_overview, code_details, utils.get_prompt_for_chapters_name())
        if chapter_names is None:
            raise "Problem getting chapter names"
        """ Do something to maintain orders of the chapters """
        chapter_contents = await llm.get_chapter_contents(init_overview, chapter_names, files, utils.get_prompt_for_chapter_contents())
        project_intro = await llm.get_intro_content(init_overview, chapter_contents, utils.get_compression_prompt(), utils.get_prompt_for_project_intro())

        document = Aidoc(repo_info, temp_dir, chapter_contents, project_intro)
        # will use path for letting user download it
        doc_name = document.create_document()
        shutil.copy(doc_name, "test_doc.docx")
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
