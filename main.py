import asyncio
import sys
from docifyai.core import model
from docifyai.services import get_repo
from docifyai.core import logger
from docifyai.utils import utils
from docifyai.core.preprocess import RepoParseFunc as repo_parse

logger = logger.Logger(__name__)


def main() -> None:
    asyncio.run(docify_run())


async def docify_run() -> None:
    logger.info("Welcome to docify-ai prototype testing")
    url = sys.argv[1]
    logger.info(f"Respo info {get_repo.get_github_repo_metadata(url)}")

    temp_dir = get_repo.clone_repo(url)

    llm = model.OpenAIHandler()

    try :
        temp_dir = get_repo.clone_repo(url)
        files = repo_parse.get_files(temp_dir)
        logger.info(f"Files: {files}")
        code_summary = await llm.code_to_text(
            utils.get_ignore_files(),
            files,
            utils.get_prompt()
        )
        logger.info(f"Code summaries returned:\n{code_summary[:5]}")

    except Exception as excinfo:
        logger.error(
            f"Exception: {excinfo}\n"
        )
    finally:
        await llm.close()

    logger.info("Docify-ai execution completes.")




