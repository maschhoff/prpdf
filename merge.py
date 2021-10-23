"""

PR PDF

Merge Pages File

2020 maschhoff github.com/maschhoff

""" 

from PyPDF2 import PdfFileMerger,PdfFileReader,PdfFileWriter
import os
from vars import *

#------------------------------------------------
# Vorder Rueckseite in einzelne PDFs
# Automatic Document Feader
def pdf_adf(frontpdfraw, backpdfraw, out_filename):

    frontpdf = PdfFileReader(open(frontpdfraw, "rb"))
    backpdf = PdfFileReader(open(backpdfraw, "rb"))

    if frontpdf.numPages==backpdf.numPages:

        output = PdfFileWriter()
        for i in range(int(frontpdf.numPages)):
            #print(i)
            output.addPage(frontpdf.getPage(i))
            output.addPage(backpdf.getPage(backpdf.numPages-i-1))
            #print(backpdf.numPages-i-1)
        with open(unknown_dir+out_filename+".pdf", "wb") as outputStream:
            output.write(outputStream)

        return "merged"

    else:
        return "page amount front/back differs"



# Alle PDFs aus Verzeichnis in eine PDF
def pdf_merge_all(allpdfs,out_filename):

    #allpdfs = [a for a in glob(in_dir+"*.pdf")]     # Liste Files aus in_dir
    pdf_anz=int(len(allpdfs))                       # Anzahl Files
    if pdf_anz >1:
        merger = PdfFileMerger() 
        for i in range(int(pdf_anz)):
            merger.append(allpdfs[i])               # alle Seiten plus

        with open(unknown_dir+out_filename+".pdf", "wb") as new_file:
            merger.write(new_file)              # alle Seiten in neues File
    else:
        print("Fehler!!! PDF Dir nicht vorhanden")


# PDF zusammenfassen aus mehreren Files alle Seiten in neues File
def pdf_merge_file(file1,file2,out_filename):
    pdf_files=[file1,file2]
    merger = PdfFileMerger() 
    for files in pdf_files:
        merger.append(files) 
    with open(unknown_dir+out_filename+".pdf", "wb") as new_file:
        merger.write(new_file)              # alle Seiten in neues File
    return "merged"

