from abc import ABC
from typing import List, Dict
from pathlib import Path
import jedi
from docifyai.core import logger
# from pygments.token import Token
# from pygments.lexers import get_lexer_by_name

from docifyai.langaugeSupport.abstractLangClass import LanguageClass

logger = logger.Logger(__name__)


class LangSupportPython(LanguageClass):

    # def tokenize(self) -> bool:
    #     lexer = get_lexer_by_name("python")
    #     tokens = list(lexer.get_tokens(self.code))
    #
    #     self.code_tokens = [value for token_type, value in tokens if token_type == Token.Name]
    #     if len(self.code_tokens) > 0:
    #         return True
    #     return False

    def get_depend_dict(self) -> Dict[Path, List[Path]]:

        depend_dict: Dict[Path: List[str]] = {}
        project = jedi.Project(self.project_path)

        for path, code in self.files.items():
            temp_list: List[Path] = []
            try:
                if str(path).split(".")[-1] == "py":
                    script = jedi.Script(code=code, project=project)
                    names = script.get_names()

                    for name in names:
                        lis_def_path = script.goto(name.line, name.column, follow_imports=True,
                                                   follow_builtin_imports=False)

                        if len(lis_def_path) > 0:

                            def_path = lis_def_path[0].module_path
                            if def_path is not None:
                                temp_list.append(Path(def_path).relative_to(self.project_path))

                    if len(temp_list) > 0:
                        depend_dict[path] = temp_list
            except Exception as excs:
                pass
                # logger.debug("error in getting python depend_dict ", excs)

        return depend_dict
