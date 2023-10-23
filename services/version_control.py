"""Git-related utilities for readme-ai"""

import os
import tempfile

import git
import requests
from pathlib import Path

from core import logger

logger = logger.Logger(__name__)


def make_request(url: str, **kwargs) -> dict:
    """Makes an HTTP request for the given remote reppsitory provider."""
    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return {}
        elif response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                f"Error retrieving repository metadata: {response.status_code}"
            )
    except requests.RequestException as excinfo:
        raise ValueError(
            f"Error retrieving repository metadata: {excinfo}"
        ) from excinfo


def get_github_repo_metadata(repo_url: str) -> dict:
    """Retrieves metadata about a Github repository"""
    api_url = parse_repo_url(repo_url, "github")
    repo_metadata = make_request(api_url)
    return repo_metadata


def clone_repo_to_temp_dir(repo_path: str) -> Path:
    temp_dir = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(repo_path, temp_dir, depth=1, single_branch=True)
        return Path(temp_dir)

    except git.GitCommandError as excinfo:
        raise ValueError(f"Git clone error: {excinfo}") from excinfo

    except Exception as excinfo:
        raise ValueError(
            f"Error cloning git repository: {excinfo}"
        ) from excinfo


def parse_repo_url(repo_url: str, provider: str) -> str:
    """Parse the repository URL and contructs the API URL."""
    parts = repo_url.rstrip("/").split("/")
    user_repo_name = f"{parts[-2]}/{parts[-1]}"

    api_url_mapping = {
        "github": f"https://github.com/repos/{user_repo_name}"
    }

    return api_url_mapping.get(provider.lower())
