#!/usr/bin/python3

import glob
import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

number_of_pages = input("Entrer le nombre de pages: ")
number_of_pages = int(number_of_pages)


def clean():
    files = glob.glob('Merge/*')
    for f in files:
        os.remove(f)
    files = glob.glob('Target/*')
    for f in files:
        os.remove(f)


def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)


def write_all_pages(input_path):
    print("Séparation des pages")
    inputpdf = PdfFileReader(open(input_path, "rb"))
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("Target/" + input_path.split("/")[1] + "_page%s.pdf" % (i + 1), "wb") as outputStream:
            output.write(outputStream)


source_pdf_files = glob.glob("Source/*.pdf")

for j in source_pdf_files:
    print("Le Nom du fichier est ", j)
    write_all_pages(j)

for p in range(1, number_of_pages + 1):
    paths = glob.glob("Target/" + "*_page%s.pdf" % str(p))
    paths.sort()
    merger('Merge/Page' + str(p) + ".pdf", paths)

paths = glob.glob('Merge/Page*.pdf')
paths.sort()
merger('Document_Final_Page.pdf', paths)

clean()
