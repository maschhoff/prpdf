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
