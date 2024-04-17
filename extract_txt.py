# A script for extraction, formating and saving txt from PDF

import re
import sys
from pdfminer.high_level import extract_text

pdf_path = sys.argv[1]
txt_path = sys.argv[2]

if len(sys.argv) != 3:
    print("Usage: python3 extract_txt.py <pdf_path> <txt_path>")

def extract_text_from_pdf(pdf_path, txt_path):
    # Load the text from PDF
    text = extract_text(pdf_path)
    
    # Create a regular expression matching one or more digits with line break - page number
    page_number = re.compile(r"\d+\r?\n")

    # Replace occurences with re.sub()
    text = re.sub(page_number, "", text)

    with open(txt_path, "w", encoding="UTF8") as file:
        file.write(text)

if __name__ == "__main__":
    extract_text_from_pdf(pdf_path, txt_path)