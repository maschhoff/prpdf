"""
from PyPDF2 import PdfFileWriter, PdfFileReader


def splitPages(inputfile,page):
    input_pdf = PdfFileReader(open(inputfile, "rb"))
    output1 = PdfFileWriter()

    #for x in range(2):
    output1.addPage(input_pdf.getPage(0))


    with open(inputfile.split(".")[0]+"_1.pdf", "wb") as output_stream1:
        output1.write(output_stream1)
    
    output2 = PdfFileWriter()

    #for y in range(3, input_pdf.numPages-1):
    output2.addPage(input_pdf.getPage(0))

    with open(inputfile.split(".")[0]+"_2.pdf", "wb") as output_stream2:
        output2.write(output_stream2)

"""

from PyPDF2 import PdfFileWriter, PdfFileReader

def split_pdf(filename,seite):
    pdf_reader = PdfFileReader(open(filename, "rb"))
    out1 = '{}_part_{}.pdf'.format(filename[:-4], 1)
    out2 = '{}_part_{}.pdf'.format(filename[:-4], 2)

    try:
        assert seite < pdf_reader.numPages
        pdf_writer1 = PdfFileWriter()
        pdf_writer2 = PdfFileWriter()

        for page in range(seite): 
            pdf_writer1.addPage(pdf_reader.getPage(page))

        for page in range(seite,pdf_reader.getNumPages()):
            pdf_writer2.addPage(pdf_reader.getPage(page))

        with open(out1, 'wb') as file1:
            pdf_writer1.write(file1)

        with open(out2, 'wb') as file2:
            pdf_writer2.write(file2)

    except AssertionError as e:
        print("Error: Seite groesser Anzahl Seiten")