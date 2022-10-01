"""

PR PDF

Split Pages File

2022 maschhoff github.com/maschhoff 

""" 

from PyPDF2 import PdfFileWriter, PdfFileReader

#Rotate a document 180 clockwise
def rotate_pages(filename):
    try:
        pdf_in = open(filename, 'rb')
        pdf_reader = PdfFileReader(pdf_in)
        pdf_writer = PdfFileWriter()

        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(180)
            pdf_writer.addPage(page)
 
        pdf_out = open(filename[:-4]+"_rotated.pdf", 'wb')
        #pdf_out = open(filename, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
    except:
        print("Error: rotation failed")

#split a document after pagenumber
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