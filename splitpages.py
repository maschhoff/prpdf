from PyPDF2 import PdfWriter, PdfReader

# Rotate all pages in a PDF 180 degrees clockwise and save as a new file
def rotate_pages(filename):
    try:
        with open(filename, 'rb') as pdf_in:
            reader = PdfReader(pdf_in)
            writer = PdfWriter()

            for page in reader.pages:
                page.rotate(180)  # Rotate page 180 degrees clockwise
                writer.add_page(page)

        output_file = filename[:-4] + "_rotated.pdf"
        with open(output_file, 'wb') as pdf_out:
            writer.write(pdf_out)

        print(f"Rotation complete: {output_file}")

    except Exception as e:
        print(f"Error: rotation failed – {e}")

# Split PDF into two parts after a given page number
def split_pdf(filename, split_after_page):
    try:
        with open(filename, "rb") as file:
            pdf_reader = PdfReader(file)

            if split_after_page >= len(pdf_reader.pages):
                raise ValueError("Split page number exceeds total pages")

            pdf_writer1 = PdfWriter()
            pdf_writer2 = PdfWriter()

            # Add pages up to split_after_page (exclusive) to first part
            for page_num in range(split_after_page):
                pdf_writer1.add_page(pdf_reader.pages[page_num])

            # Add remaining pages to second part
            for page_num in range(split_after_page, len(pdf_reader.pages)):
                pdf_writer2.add_page(pdf_reader.pages[page_num])

            out1 = f'{filename[:-4]}_part_1.pdf'
            out2 = f'{filename[:-4]}_part_2.pdf'

            with open(out1, 'wb') as file1:
                pdf_writer1.write(file1)

            with open(out2, 'wb') as file2:
                pdf_writer2.write(file2)

            print(f"Split complete: {out1}, {out2}")

    except Exception as e:
        print(f"Error splitting PDF: {e}")
