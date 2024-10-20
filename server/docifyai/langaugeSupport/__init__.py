# will use this for giving a class for diffrent lang from the languageSupport base class
from docifyai.langaugeSupport.abstractLangClass import LanguageClass
from docifyai.langaugeSupport.python import LangSupportPython


def get_lang_support(name, files, project_path):
    if name == "python":
        return LangSupportPython(files, project_path)
