import tempfile

import git
import requests
from pathlib import Path
from docifyai.core import logger

logger = logger.Logger(__name__)


def get_github_repo_metadata(repo_url: str, auth_token: str) -> dict:
    """Retrieves metadata of a GitHub repository"""
    parts = repo_url.rstrip("/").split("/")
    user_repo_name = f"{parts[3]}/{parts[4]}"
    api_url = f"https://api.github.com/repos/{user_repo_name}"
    header = {
        'Authorization': f'token {auth_token}',
    }

    try:
        response = requests.get(api_url, headers=header)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                f"Error retrieving repository metadata: {response.status_code}"
            )
    except requests.RequestException as excinfo:
        raise ValueError(
            f"Error retrieving repository metadata: {excinfo}"
        ) from excinfo


def clone_repo(repo_url: str, branch: str) -> str:
    """clone the repo to temporary folder"""
    temp_dir = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(repo_url, temp_dir, branch=branch, depth=1, single_branch=True)
        # may need to remove the .git folder in the temp folder

        return temp_dir
    except git.GitCommandError as excinfo:
        raise ValueError(f"Git clone error: {excinfo}") from excinfo

    except Exception as excinfo:
        raise ValueError(f"Error cloning git repo: {excinfo}") from excinfo

# may need to change the file permission, so that app can use it
# also we have to check if git command is available or not before using python git
