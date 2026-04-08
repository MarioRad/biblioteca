from PyPDF2 import PdfReader
import re
import os

def extract_metadata(pdf_path):
    reader = PdfReader(pdf_path)
    info = reader.metadata

    title= info.title if info and info.title else None,
    author= info.author if info and info.author else None,

 # 👇 fallback inteligente
    if not title:
        title = extract_title_from_filename(pdf_path)

    return {
        "title": title,
        "author": author,
    }
   
      


def get_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages[:3]:
        text += page.extract_text() or ""

    return text


def extract_isbn(text):
    pattern = r"(97(8|9))?\d{9}(\d|X)"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_title_from_filename(pdf_path):
    filename = os.path.basename(pdf_path)

    # quitar extensión
    name = os.path.splitext(filename)[0]

    # reemplazar separadores comunes
    name = name.replace("_", " ").replace("-", " ")

    # eliminar cosas tipo (2020), [ebook], etc.
    name = re.sub(r"\(.*?\)|\[.*?\]", "", name)

    # limpiar espacios dobles
    name = re.sub(r"\s+", " ", name).strip()

    return name