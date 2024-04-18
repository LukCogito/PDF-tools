# A script for extraction, formatting and saving txt from PDF

import re
import sys
import statistics
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

    # Replace double spaces with single spaces in text
    text = text.replace("  ", " ")

    # Split text to lines
    text_splitted = text.splitlines()
    # Create a list for text lines without the lines containing only line breaks
    text_splitted_without_empty_lines = []
    
    # Iterrate over the splitted text
    for line in text_splitted:
        # If line isn't empty
        if line != "\n" or line != "":
            # Append the line
            text_splitted_without_empty_lines.append(line)

    # Use text_splitted var, becaus it's shorter and easier to write without typo
    text_splitted = text_splitted_without_empty_lines
    # Create a list for lines lengths
    lines_lengths = []

    # Iterrate over the splitted text
    for line in text_splitted:
        # Line length is the lengt of the list of words on each line
        line_length = len(line.split())
        # Lines lengths is list of length of each line in text
        lines_lengths.append(line_length)

    # Title treshold is rounded value of first six-tile of the text length distribution
    title_threshold = round(statistics.quantiles(lines_lengths, n=6)[0])
    # Create a new string var for output text
    output = ""

    # Iterrate over the splitted text and lengths of its lines
    for line, length in zip(text_splitted, lines_lengths):
        # If length of iterrated line equals or is bellow the threshold 
        if length <= title_threshold:
            # Add it to the output as separate line (we assume that it's title)
            output += line + "\n"
        # In other cases, add it to an existing line
        else:
            output += line + " "

    with open(txt_path, "w", encoding="UTF8") as file:
        file.write(output)

if __name__ == "__main__":
    extract_text_from_pdf(pdf_path, txt_path)
