from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from typing import Dict, Any
import requests
from docifyai.core import logger
from docifyai.document import contents

logger = logger.Logger(__name__)


class Aidoc:
    def __init__(self,
                 # repo_summary: Dict[str, str],
                 repo_data: Any) -> None:
        # self.code_summary_data = repo_summary
        self.repo_data = repo_data

        # we may use non default template in future
        self.doc = Document()

    def create_document(self) -> str:
        self.add_first_page()
        self.add_content_page()
        self.doc.save("documentFileFirst.docx")
        return "documentFileFirst.docx"

    def add_first_page(self) -> None:
        """"""
        doc = self.doc
        repo_data = self.repo_data
        title_head = doc.add_heading(repo_data["name"], 0)
        title_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # title_run = title_head.runs[0]
        # title_run.add_text(repo_data["description"])
        # title_run.font.size = 13
        # title_run.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_para = doc.add_paragraph(repo_data["description"])
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # for project info
        lang_res = requests.get(repo_data["languages_url"])
        lang_used = {}
        if lang_res.status_code == 200:
            lang_used = lang_res.json()
        lang_str = ""
        for lang, count in lang_used.items():
            lang_str = f"{lang_str}{lang}:{count}\n"

        """Improve the formatting of the project info"""
        """also add avatar and licence type"""
        doc.sections[-1].start_type
        section = doc.sections[-1]
        section.footer_distance = Pt(36)
        section.footer_line = False

        footer = section.footer
        owner_name = {repo_data["owner"]["login"]}
        fork_count = {repo_data["forks_count"]}
        info_for_doc = f"Owner:{owner_name}\nLanguages Used:\t{lang_str}\nFork Count: {fork_count}"
        footer_para = footer.paragraph = footer.add_paragraph(info_for_doc)
        footer_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        # doc.save("documentFileFirst.docx")

        # return "documentFileFirst.docx"

    def add_content_page(self) -> None:
        contents_page = contents.ContentGen(
            self.doc,
            "/home/tabish/Programming/PycharmProjects/docify-ai"  # for testing

        )
        contents_page.add_content_page()

    def add_intro_page(self) -> None:
        doc = self.doc
