"""Not in use right now, will be used in future"""

from typing import List, Dict

from docifyai.core import logger
logger = logger.Logger(__name__)

def get_file_parser() -> Dict[str, callable]:
    """Returns a dictionary of callable file parser methods"""
    return {
        # "build.gradle": parse_gradle,
        # "pom.xml": parse_maven,
        # "Cargo.toml": parse_cargo_toml,
        # "Cargo.lock": parse_cargo_lock,
        # "go.mod": parse_go_mod,
        # "go.sum": parse_go_mod,
        # "requirements.txt": parse_requirements_file,
        # "environment.yaml": parse_conda_env_file,
        # "environment.yml": parse_conda_env_file,
        # "Pipfile": parse_pipfile,
        # "Pipfile.lock": parse_pipfile_lock,
        # "poetry.lock": parse_poetry_lock,
        # "pyproject.toml": parse_pyproject_toml,
        # "package.json": parse_package_json,
        # "yarn.lock": parse_yarn_lock,
        # "package-lock.json": parse_package_lock_json,
        # "CMakeLists.txt": parse_cmake,
        # "Makefile.am": parse_makefile_am,
        # "configure.ac": parse_configure_ac,
        # "docker-compose.yaml": parse_docker_compose,
    }

