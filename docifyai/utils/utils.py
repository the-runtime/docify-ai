from pathlib import Path
from typing import Dict, Tuple, List
from docifyai.core import logger
import json

logger = logger.Logger(__name__)


def get_json_from_gpt_response(data: str) -> Dict:
    """Use try and except to find if the response is json or it failed to generated a valid json or not"""
    real_end = data.rfind("}")
    real_start = data.find("{")
    ret_string = data[real_start: real_end + 1]
    return json.JSONDecoder().decode(ret_string)


def dict_to_json(data: Dict) -> str:
    return json.JSONEncoder().encode(data)


def change_tuple_to_dict(sample: List[Tuple[str, str]]) -> Dict[str, str]:
    resp_dict = {}
    for r in sample:
        resp_dict[r[0]] = r[1]
    return resp_dict


def get_working_path_of_project(repo_path: str, base_folder: Path) -> Path:
    logger.debug(base_folder.joinpath(repo_path))
    base_folder.joinpath(repo_path)
    return base_folder.joinpath(repo_path)


def get_role_content(val: int) -> str:
    """Need to change, can use something like enums"""
    if val == 0:
        # for code info
        return """You are a person who is very good at giving overview of code snippet without getting into the 
        technical details."""
    elif val == 1:
        # for inti info
        return """You are a software developer who is making an overview of a software project."""
    elif val == 2:
        # for chapter name
        return """You are a book editor which is experienced in editing books in the domain of software engineering."""
    elif val == 3:
        # for chapter contents
        return """You are a book writer who writes books about software engineering and software design engineering."""
    elif val == 4:
        # for project intro
        # may need to change for better result
        return """You are a Project manager and a Business Analyst model."""


def get_prompt_for_code_info() -> str:
    """Need a better prompt as 3 lines is not sufficient for most real project code files"""
    return """Read the given code file and give a summary. Focus on the functionality and not on the implementation 
    of the code. Limit your response to a maximum of 400 characters (including spaces).
    Path: {0}
    Code: {1}
    """


def get_prompt_for_init_info() -> str:
    return """Consider the codebase as a whole and analyze the structural design of the system and try to find the
    purpose of the project and not focus on the configurations and other things.
    Try to find the type of the application it is and read the info provided again to make a proper description of it.
    Code Info:{0}
    """


def get_prompt_for_chapters_name() -> str:
    # Consider the codebase as a whole and analyze the structural design of the system and give the chapter for
    # better understanding of the architecture.

    return """Read the given Purpose and code file info of a software project and return in json the chapters
    information document of the project should contain, it should have files names (as a list) associated with each chapter.
    While giving chapter names the focus should be on how a new developer will understand the project/application.
    Don't focus on the configuration, setup, error handling and testing of the project only focus on explaining the design of the project.
    Response format should be like {{"chaptername1": ["file1","file2", ...], "chaptername2": ["file1", ....], ....}}
    Purpose: {0}
    Code Info: {1}"""


def get_prompt_for_chapter_contents() -> str:
    return """"Produce the contents of the chapter of a software project given the project purpose and the files 
    associated with the chapter.Focus on the flow of the project. Avoid using code snippet and also be concise.
    Keep things clean and simple.
    Chapter name: {0} Purpose: {1} Files: {2}"""


def get_compression_prompt() -> str:
    return """Summarize the given chapter to a point where the summary can be used to generate the introduction to 
    project document.
    Purpose of the project:{0}
    Chapter Contents: {1}"""


def get_prompt_for_project_intro() -> str:
    return """Give a detailed introduction of the project/application given the purpose and 
    summary of all the chapter it contains
    Purpose of the project: {0}
    Chapter Overviews: {1}
    """


# used in older versions of docify-ai // starts here
def get_intro_prompt() -> str:
    return """Give the purpose of the project and tell about what it does and serves to end user. Also offer a 
    comprehensive architectural design and other aspects of the software project that encapsulates the core 
    functionalities of the project given the details of the packages and files inside it. Details: {0}"""


def get_folders_prompt() -> str:
    return """Offer a detailed higher level (don't talk about implementation and programming) examination of what the 
    purpose of the folder/package of which the implementation details is provided below along with its relative 
    position. Assume it is for normal non technical person. {0}"""


def get_implementation_prompt() -> str:
    return """Offer a brief explanation of the code,
    taking reference of point from the 'Files referenced from the main file'' Path: {0} Contents: {1} Files 
    referenced from the main file:{2}
    respond in no more than 200 words.
    """


# end here

def should_ignore(file_path: Path) -> bool:
    """Filters out files that should be ignored"""
    ignore_files = get_ignore_files()

    for directory in ignore_files["directories"]:
        if directory in file_path.parts:
            logger.debug(f"Ignoring directory: {file_path}")
            return True

    if file_path.name in ignore_files["files"]:
        logger.debug(f"Ignoring file: {file_path}")
        return True

    if file_path.suffix[1:] in ignore_files["extensions"]:
        logger.debug(f"Ignoring file: {file_path}")
        return True

    return False


def get_ignore_files() -> Dict[str, list[str]]:
    directories = [
        ".DS_Store",
        ".dvc",
        ".eggs",
        ".git",
        ".hg",
        ".idea",
        ".pytest_cache",
        ".svn",
        ".tox",
        ".vscode",
        "assets",
        "css",
        "bootstrap"
        "data",
        "dist",
        "docs",
        "htmlcov",
        "imgs",
        "media",
        "static",
        "tests",
        "testing",
        "tools",
        "__pycache__",
        "Examples",
    ]
    extensions = [
        'ttf',
        'otf',
        # 'apk',
        # 'app',
        'bak',
        'bakup',
        'bmp',
        'bz2',
        'cache',
        'cert',
        'cfg',
        'class',
        'css'
        'csv',
        'dat',
        'db',
        'dll',
        'docx',
        'dylib',
        'egg',
        'env',
        'env.example',
        'env.local',
        'env.production',
        'env.test',
        'eot',
        'exe',
        'gif',
        'gitignore',
        'gz',
        'h5',
        'ico',
        'iml',
        'ini',
        'jar',
        'jpeg',
        'jpg',
        'json',
        'json5',
        'jsonl',
        'key',
        'lockb',
        'log',
        'md',
        'mp3',
        'mp4',
        'o',
        'old',
        'p',
        'p12',
        'pdf',
        'pem',
        'pickle',
        'pkl',
        'png',
        'properties',
        'pyc',
        'pyd',
        'pyo',
        'rkt',
        'sav',
        'secret',
        'so',
        'svg',
        'swp',
        'tar',
        'tif',
        'tiff',
        'tmp',
        'tsv',
        'webp',
        'woff',
        'woff2',
        'xls',
        'xlsx',
        'xml',
        'zip',
        'zst',
    ]

    files = [
        ".babelrc",
        ".dockerignore",
        ".dvcignore",
        ".editorconfig",
        ".flake8",
        ".git",
        ".gitattributes",
        ".gitignore",
        ".gitkeep",
        ".gitlab-ci",
        ".gitmodules",
        ".npmignore",
        ".pre-commit-config.yaml",
        ".prettierrc",
        ".project-root",
        ".whitesource",
        "AUTHORS",
        "CHANGELOG",
        "CODE_OF_CONDUCT",
        "CONTRIBUTING",
        "LICENSE",
        "LICENSE-APACHE",
        "LICENSE_APACHE-2.0",
        "LICENSE-MIT",
        "MANIFEST",
        "README",
        "README.md",
        "appimage",
        "bundle_dmg",
        "gradlew",
        "icon.ico~dev",
        "__init__.py",
        "start",
        "test_binary",
    ]

    ignore_files = {
        "directories": directories,
        "extensions": extensions,
        "files": files
    }

    return ignore_files
