from abc import ABC, abstractmethod
from typing import Dict, List
from pathlib import Path


class LanguageClass(ABC):

    def __init__(self, files: Dict[Path, str], project_path: Path):
        self.project_path = str(project_path)
        self.files = files

    # @abstractmethod
    # def tokenize(self):
    #     pass

    @abstractmethod
    def get_depend_dict(self) -> Dict[Path, List[Path]]:
        pass
