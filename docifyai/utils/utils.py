from pathlib import Path
from typing import Dict
from docifyai.core import logger

logger = logger.Logger(__name__)


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

    if file_path.suffix[1:]in ignore_files["extensions"]:
        logger.debug(f"Ignoring file: {file_path}")
        return True

    return False


def get_ignore_files() -> Dict[str,list[str]]:
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
        # 'apk',
        # 'app',
        'bak',
        'bakup',
        'bmp',
        'bz2',
        'cache',
        'cert',
        # 'cfg',
        'class',
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
        # 'json',
        # 'json5',
        # 'jsonl',
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
