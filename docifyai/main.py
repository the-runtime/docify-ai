import sys
from docifyai.core import model
from docifyai.services import get_repo
from docifyai.core import logger

logger = logger.Logger(__name__)


def main():
    logger.info("Welcome to docify-ai prototype testing")
    url = sys.argv[1]
    logger.info(f"Respo info {get_repo.get_github_repo_metadata(url)}")

    temp_dir = get_repo.clone_repo(url)
