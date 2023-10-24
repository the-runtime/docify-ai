from typing import List, Dict, Generator, Tuple
from pathlib import Path
from core import tokens


class RepositoryParser:

    def __int__(
            self,
            # config: settings.AppConfig,
            # conf_helper: settings.ConfigHelper,
    ):

        # self.config = config
        self.encoding_name = "cl100k_base"

    def analyze(self, repo_path: str) -> List[Dict]:
        """Analyze a local or remote git repository"""
        contents = self.generate_contents(repo_path)
        contents = self.tokenize_content(contents)
        contents = self.process_language_mapping(contents)
        return contents

    def generate_contents(self, repo_path: str) -> List[Dict]:
        """Generates a List of Dict of file information"""
        repo_path = Path(repo_path)

        data = list(self.generate_file_info(repo_path))

        contents = []

        for name, path, content in data:
            extension = Path(name).suffix.lstrip(".")
            contents.append(
                {
                    "name": name,
                    "path": path,
                    "content": content,
                    "extension": extension,
                }
            )
        return contents

    def generate_file_info(
            self, repo_path: Path
    ) -> Generator[Tuple[str, Path, str], None, None]:
        """Generates a tuple of file information"""
        for file_path in repo_path.rglob("*"):
            # if utils.should_ignoe(self.config_helper, file_path):
            #     continue

            if file_path.is_file():
                try:
                    with file_path.open(encoding="utf-8") as file:
                        content = file.read()
                    relative_path = file_path.relative_to(repo_path)
                    yield file_path.name, relative_path, content
                except UnicodeDecodeError:
                    continue

    def get_file_contents(self, contents: Dict) -> Dict[str, str]:
        """Extracts the file contents from the list of dicts."""
        return {content["path"]: content["content"] for content in contents}

    def process_language_mapping(self, contents: List[Dict]) -> List[Dict]:
        """Maps file extensions to their programming languages."""
        for content in contents:
            content["language"] = self.language_names.get(
                content["extension"], ""
            ).lower()
            setup = self.language_setup.get(content["language"], "")
            setup = setup if isinstance(setup, list) else [None, None]
            while len(setup) < 3:
                setup.append(None)
            content["install"], content["run"], content["test"] = setup
        return contents

    def tokenize_content(self, contents: List[Dict]) -> List[Dict]:
        """Tokenize the content of each file"""
        for content in contents:
            content["tokens"] = tokens.get_token_count(
                contents["content"], self.encoding_name
            )
        return contents
