from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
from vars import *

#------------------------------------------------
# Merge front and back PDFs page by page (like an Automatic Document Feeder)
def pdf_adf(front_pdf_path, back_pdf_path, out_filename):
    front_pdf = PdfReader(open(front_pdf_path, "rb"))
    back_pdf = PdfReader(open(back_pdf_path, "rb"))

    if len(front_pdf.pages) == len(back_pdf.pages):
        output = PdfWriter()
        for i in range(len(front_pdf.pages)):
            output.add_page(front_pdf.pages[i])
            # Add back pages in reverse order to simulate back side
            output.add_page(back_pdf.pages[len(back_pdf.pages) - i - 1])

        output_path = os.path.join(unknown_dir, out_filename + ".pdf")
        with open(output_path, "wb") as output_stream:
            output.write(output_stream)

        return "merged"
    else:
        return "page count front/back differs"


# Merge all PDFs from a list of files into one PDF
def pdf_merge_all(pdf_file_list, out_filename):
    pdf_count = len(pdf_file_list)
    if pdf_count > 1:
        merger = PdfMerger()
        for pdf_file in pdf_file_list:
            merger.append(pdf_file)

        output_path = os.path.join(unknown_dir, out_filename + ".pdf")
        with open(output_path, "wb") as new_file:
            merger.write(new_file)
    else:
        print("Error!!! PDF directory does not contain multiple files")


# Merge two PDF files into one new PDF file
def pdf_merge_file(file1, file2, out_filename):
    pdf_files = [file1, file2]
    merger = PdfMerger()
    for file in pdf_files:
        merger.append(file)

    output_path = os.path.join(unknown_dir, out_filename + ".pdf")
    with open(output_path, "wb") as new_file:
        merger.write(new_file)

    return "merged"
