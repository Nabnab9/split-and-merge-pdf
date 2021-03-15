#!/usr/bin/python3

import glob
import os
import re

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from PyPDF2.pdf import PageObject
from ordered_enum import OrderedEnum

from typing import Dict, Set


class PageType(OrderedEnum):
    SUPPLIER = 1
    LOGISTIC_PARTNER = 2
    KANBAN = 3
    PALLET = 4
    OTHER = 5


class PagePdf:
    page_code: str
    page_object: PageObject
    page_text_content: str
    page_type: PageType

    def __init__(self, page_object):
        self.page_object = page_object
        self.page_text_content = page_object.extractText()
        self.page_type = self.get_type()
        self.page_code = self.get_code()

    def search(self, str_to_find: str) -> bool:
        return str_to_find in self.page_text_content

    def get_type(self) -> PageType:
        if self.search("SUPPLIER MANIFEST"):
            return PageType.SUPPLIER
        if self.search("LOGISTIC PARTNER MANIFEST"):
            return PageType.LOGISTIC_PARTNER
        if self.search("KANBAN"):
            return PageType.KANBAN
        if self.search("PALLET"):
            return PageType.PALLET
        return PageType.OTHER

    def get_code(self) -> str:
        regex = r'20\d{4}(\d{4})'
        code_search = re.search(regex, self.page_text_content, re.IGNORECASE)
        code = '0000'
        if code_search:
            code = code_search.group(1)
        return code


def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as file_object:
        pdf_merger.write(file_object)


def clean():
    files = glob.glob('Merge/*')
    for f in files:
        os.remove(f)
    files = glob.glob('Source/*')
    for f in files:
        os.remove(f)


class SplitAndMergePdf:
    nb_doc_expected: int
    lots: Dict[str, Set[PagePdf]]

    def __init__(self, nb_doc_expected):
        self.nb_doc_expected = nb_doc_expected
        self.lots = {}

    def write_all_pages(self, input_path):
        input_pdf = PdfFileReader(open(input_path, "rb"))
        for i in range(input_pdf.numPages):
            page = input_pdf.getPage(i)
            page_pdf = PagePdf(page_object=page)

            if page_pdf.page_code not in self.lots:
                self.lots[page_pdf.page_code] = set()
            self.lots[page_pdf.page_code].add(page_pdf)

    def run(self):

        source_pdf_files = glob.glob("Source/*.pdf")

        for j in source_pdf_files:
            self.write_all_pages(j)

        for code, pages_pdf in self.lots.items():

            output = PdfFileWriter()
            for p in sorted(pages_pdf, key=lambda page: page.page_type):
                output.addPage(p.page_object)
            for i in range(self.nb_doc_expected - len(pages_pdf)):
                output.addBlankPage()
            with open(f"Merge/Page_{code}.pdf", "wb") as outputStream:
                output.write(outputStream)

        paths = glob.glob('Merge/Page_*.pdf')
        paths.sort()
        merger('Document_Final.pdf', paths)

        clean()


if __name__ == "__main__":
    split_and_merge_pdf = SplitAndMergePdf(nb_doc_expected=4)
    split_and_merge_pdf.run()
