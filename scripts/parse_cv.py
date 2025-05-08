import fitz  # PyMuPDF
import os
import yaml
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def main():
    cv_folder = Path("cv_input/")
    pdf_files = list(cv_folder.glob("*.pdf"))

    if len(pdf_files) == 0:
        raise FileNotFoundError("No PDF file found in 'cv_input/' folder.")
    elif len(pdf_files) > 1:
        raise ValueError("Multiple PDF files found in 'cv_input/'. Please keep only one.")
    else:
        cv_path = pdf_files[0]
        
    extracted_text = extract_text_from_pdf(cv_path)

    output_path = Path("data/cv_parsed.txt")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"[✔] CV parsed and saved to: {output_path}")

if __name__ == "__main__":
    main()