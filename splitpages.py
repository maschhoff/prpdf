"""

PR PDF

Split Pages File

2022 maschhoff github.com/maschhoff 

""" 

from PyPDF2 import PdfWriter, PdfReader

#Rotate a document 180 clockwise
def rotate_pages(filename):
    try:
        pdf_in = open(filename, 'rb')
        pdf_reader = PdfReader(pdf_in)
        pdf_writer = PdfWriter()

        for pagenum in range(len(pdf_reader.pages)):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(180)
            pdf_writer.add_page(page)
 
        pdf_out = open(filename[:-4]+"_rotated.pdf", 'wb')
        #pdf_out = open(filename, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
    except:
        print("Error: rotation failed")

#split a document after pagenumber
def split_pdf(filename,seite):
    pdf_reader = PdfReader(open(filename, "rb"))
    out1 = '{}_part_{}.pdf'.format(filename[:-4], 1)
    out2 = '{}_part_{}.pdf'.format(filename[:-4], 2)

    try:
        assert seite < len(pdf_reader.pages)
        pdf_writer1 = PdfWriter()
        pdf_writer2 = PdfWriter()

        for page in range(seite): 
            pdf_writer1.add_page(pdf_reader.pages[page])

        for page in range(seite,len(pdf_reader.pages)):
            pdf_writer2.add_page(pdf_reader.pages[page])

        with open(out1, 'wb') as file1:
            pdf_writer1.write(file1)

        with open(out2, 'wb') as file2:
            pdf_writer2.write(file2)

    except AssertionError as e:
        print("Error: Seite groesser Anzahl Seiten")