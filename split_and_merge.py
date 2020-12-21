#!/usr/bin/python3

import glob
import os
import re

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

codes = set()
width = 0
height = 0


def clean():
    files = glob.glob('Merge/*')
    for f in files:
        os.remove(f)
    files = glob.glob('Target/*')
    for f in files:
        os.remove(f)
    files = glob.glob('Source/*')
    for f in files:
        os.remove(f)


def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)


def write_all_pages(input_path, date):
    inputpdf = PdfFileReader(open(input_path, "rb"))
    for i in range(inputpdf.numPages):
        page = inputpdf.getPage(i)
        width = page.mediaBox[2]
        height = page.mediaBox[3]
        page_content = page.extractText()

        code = get_file_code(page_content, date)
        codes.add(code)

        doc_type = get_doc_type(page_content)

        output = PdfFileWriter()
        output.addPage(page)
        with open("Target/"
                  + input_path.split("/")[1]
                  + "_page_"
                  + doc_type
                  + "_"
                  + code
                  + ".pdf",
                  "wb") as outputStream:
            output.write(outputStream)


def get_file_code(page_content, date):
    regex = r'' + date + r'(\d{4})'
    code_search = re.search(regex, page_content, re.IGNORECASE)
    code = '0000'
    if code_search:
        code = code_search.group(1)
        # print(code)
    return code


def get_doc_type(page_content):
    manifest_type = "normal"
    manifest_type_search = re.search(r'(SUPPLIER MANIFEST)', page_content)
    if manifest_type_search:
        manifest_type = "supplier"
    else:
        manifest_type_search = re.search(r'(LOGISTIC PARTNER MANIFEST)', page_content)
        if manifest_type_search:
            manifest_type = "logistic_partner"
    return manifest_type


def run(date, nb_doc_attendu):

    source_pdf_files = glob.glob("Source/*.pdf")

    for j in source_pdf_files:
        write_all_pages(j, date)

    for c in codes:

        paths = glob.glob("Target/" + "*" + "%s.pdf" % str(c))
        if len(paths) < nb_doc_attendu:
            nb_white_page = nb_doc_attendu - len(paths)
            for blank in range(nb_white_page):
                output = PdfFileWriter()
                output.insertBlankPage(width=width, height=height)
                with open("Target/"
                          + "page_"
                          + "blank"
                          + "_"
                          + str(blank)
                          + "_"
                          + c
                          + ".pdf",
                          "wb") as outputStream:
                    output.write(outputStream)

        paths = glob.glob("Target/" + "*" + "%s.pdf" % str(c))
        paths.sort()
        output_file_path = "Merge/Page_" + str(c) + ".pdf"

        merger(output_file_path, paths)

    paths = glob.glob('Merge/Page_*.pdf')
    paths.sort()
    merger('Document_Final.pdf', paths)

    clean()


if __name__ == "__main__":
    run(date='202012', nb_doc_attendu=4)
