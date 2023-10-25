from typing import List, Dict, Tuple, Generator

from pathlib import Path
import logger
class RepositoryParser:

    def __init__(self):
        self.hello = "testing"

    def analyze(self, repo_path: str) -> List[Dict]:
        """Analyzes a local git repository"""
        return [{}]

    def generate_contents(self, repo_path) -> List[Dict]:
        """Generates a list of Dict of file information"""
        repo_path = Path(repo_path)

        data = list(self.gerate)

    def generate_file_info(self, repo_path: Path) -> Generator[Tuple[str, Path, str], None, None]:
        """Generates a tuple of file information"""
        for file_path in repo_path.rglob("*"):

