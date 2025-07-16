"""

PR PDF

Merge Pages File 

2020 maschhoff github.com/maschhoff

""" 

from PyPDF2 import PdfReader,PdfWriter, PdfMerger #PdfFileMerger
import os
from vars import *

#------------------------------------------------
# Vorder Rueckseite in einzelne PDFs
# Automatic Document Feader
def pdf_adf(frontpdfraw, backpdfraw, out_filename):

    frontpdf = PdfReader(open(frontpdfraw, "rb"))
    backpdf = PdfReader(open(backpdfraw, "rb"))

    if len(frontpdf.pages)==len(backpdf.pages):

        output = PdfWriter()
        for i in range(int(len(frontpdf.pages))):
            #print(i)
            output.add_page(frontpdf.pages[i])
            output.add_page(backpdf.pages[len(backpdf.pages)-i-1])
            #print(backpdf.pages-i-1)
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
        merger = PdfMerger() 
        for i in range(int(pdf_anz)):
            merger.append(allpdfs[i])               # alle Seiten plus

        with open(unknown_dir+out_filename+".pdf", "wb") as new_file:
            merger.write(new_file)              # alle Seiten in neues File
    else:
        print("Fehler!!! PDF Dir nicht vorhanden")


# PDF zusammenfassen aus mehreren Files alle Seiten in neues File
def pdf_merge_file(file1,file2,out_filename):
    pdf_files=[file1,file2]
    merger = PdfMerger() 
    for files in pdf_files:
        merger.append(files) 
    with open(unknown_dir+out_filename+".pdf", "wb") as new_file:
        merger.write(new_file)              # alle Seiten in neues File
    return "merged"

