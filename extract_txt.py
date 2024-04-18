# A script for extraction, formatting and saving txt from PDF
# Author:
#  _          _       ____            _ _        
# | |   _   _| | __  / ___|___   __ _(_) |_ ___  
# | |  | | | | |/ / | |   / _ \ / _` | | __/ _ \ 
# | |__| |_| |   <  | |__| (_) | (_| | | || (_) |
# |_____\__,_|_|\_\  \____\___/ \__, |_|\__\___/ 
#                               |___/

import re
import os
import sys
import spacy
from pdfminer.high_level import extract_text

pdf_path = sys.argv[1]
txt_path = sys.argv[2]
lang = sys.argv[3]
title_threshold = int(sys.argv[4])

if len(sys.argv) != 5:
    print("Usage: python3 extract_txt.py <pdf_path> <txt_path> <lang> <tittle_threshold>")
    exit(1)

if not os.path.isdir(pdf_path):
    print(f"Invalid file path '{pdf_path}'")
    exit(1)

if lang != "cs" or lang != "en":
    print("Language must be 'cs' or 'en'.")
    exit(1)

# Try to load lang_core_web_sm model for nlp
try:
    nlp = spacy.load(f"{lang}_core_web_sm")
# If it fails, just intall it and chill
except OSError:
    print(f"Model '{lang}_core_web_sm' is not installed; installing...")
    spacy.cli.download(f"{lang}_core_web_sm")
    nlp = spacy.load(f"{lang}_core_web_sm")

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

    # Create a new string var for output text
    output = ""

    # Iterrate over the splitted text and lengths of its lines
    for line, length in zip(text_splitted, lines_lengths):
        # If length of iterrated line equals or is bellow the threshold 
        if length <= title_threshold:
            # If output isn't empty
            if output != "":
                # Add it to the output as separate line (we assume that it's title)
                output += "\n" + line + "\n"
            else:
                output += line + "\n"
        # In other cases, add it to an existing line
        else:
            output += line + " "

    with open(txt_path, "w", encoding="UTF8") as file:
        file.write(output)

    print(f"Text file saved to {txt_path}")

if __name__ == "__main__":
    extract_text_from_pdf(pdf_path, txt_path)
