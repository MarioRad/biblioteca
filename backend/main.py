import os
from fastapi import FastAPI, BackgroundTasks
from services.pdf_service import extract_metadata, get_text_from_pdf, extract_isbn
from services.cover_service import get_cover
from services.db_service import save_pdf

app = FastAPI()
PDF_PATH = os.getenv("PDF_PATH", "/backend/libros")

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

@app.get("/")
def read_root():
    return {"status": "Backend running", "folder": PDF_PATH}

@app.post("/scan")
def start_scan(background_tasks: BackgroundTasks):
    # Esto lanza el scanner sin bloquear la API
    background_tasks.add_task(scan_folder, PDF_PATH)
    return {"message": "Escaneo iniciado en segundo plano"}
