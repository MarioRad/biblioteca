import os
from services.pdf_service import extract_metadata, get_text_from_pdf, extract_isbn
from services.cover_service import get_cover
from services.db_service import save_pdf
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def process_pdf(pdf_path):
    print(f"Procesando: {pdf_path}")

    meta = extract_metadata(pdf_path)

    text = get_text_from_pdf(pdf_path)
    isbn = extract_isbn(text)

    cover_url = get_cover(meta, isbn, pdf_path)

    meta["isbn"] = isbn
    meta["cover_url"] = cover_url

    save_pdf(meta, pdf_path)


def scan_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                process_pdf(os.path.join(root, file))

#if __name__ == "__main__":
#    scan_folder(PDF_PATH)
if __name__ == "__main__":
    if os.path.exists(PDF_PATH):
        print(f"Éxito: La carpeta existe. Contenido: {os.listdir(PDF_PATH)}")
    else:
        print(f"Error: No encuentro la ruta {PDF_PATH}")