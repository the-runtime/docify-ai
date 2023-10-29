from typing import List, Dict, Tuple, Generator
from pathlib import Path

from docifyai.core import tokens
from docifyai.utils import utils
from docifyai.core import logger

logger = logger.Logger(__name__)


class RepoParseFunc:
    """Functions for processing of the input codebase"""
    @classmethod
    def analyze(cls, repo_path: str) -> List[Dict]:
        """Analyzes a local git repository"""
        contents = cls.generate_contents(repo_path)
        contents = cls.tokenize_contents(contents)
        # language mapping should also be here, for language server
        return contents

    @classmethod
    def generate_contents(cls, repo_path: str) -> List[Dict]:
        """Generates a list of Dict of file information"""
        p = Path(repo_path)
        repo_path = p

        data = list(cls.generate_file_info(repo_path))

        contents = []
        for name, path, content in data:
            extension = Path(name).suffix.lstrip(".")
            contents.append({
                "name": name,
                "path": path,
                "content": content,
                "extension": extension
            })
        return contents

    @classmethod
    def get_files(cls, repo_path: str) -> dict[Path, str]:
        contents = cls.analyze(repo_path)
        retobj = {content["path"]: content["content"] for content in contents}
        return retobj


    @staticmethod
    def generate_file_info(repo_path: Path) -> Generator[Tuple[str, Path, str], None, None]:
        """Generates a tuple of file information"""
        for file_path in repo_path.rglob("*"):
            if utils.should_ignore(file_path):
                continue
            if file_path.is_file():
                try:
                    with file_path.open(encoding="utf-8") as file:
                        contents = file.read()
                    relative_path = file_path.relative_to(repo_path)
                    yield file_path.name, relative_path, contents
                except UnicodeDecodeError as excinfo:
                    logger.error(f"Error decoding file to utf-8 file:{file_path}, error:{excinfo}")
                    continue

    @staticmethod
    def tokenize_contents(contents: List[Dict]) -> List[Dict]:
        """Tokenize the contents of each file
        not tokenizing tough, just counting the tokens"""

        for content in contents:
            content["tokens"] = tokens.get_token_count(
                content["content"], tokens.encoding_name_for_model("gpt-3.5-turbo")
            )
        return contents

    # process language mapping needs to implemented
