# pdf_loader.py

import PyPDF4

def load_pdf_content(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF4.PdfFileReader(file)
        total_pages = pdf_reader.getNumPages()
        pdf_content = ""

        for page in range(total_pages):
            pdf_content += pdf_reader.getPage(page).extractText()

    return pdf_content
