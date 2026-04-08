from db.supabase_client import supabase

def save_pdf(meta, pdf_path):
    data = {
        "title": meta.get("title"),
        "author": meta.get("author"),
        "isbn": meta.get("isbn"),
        "cover_url": meta.get("cover_url"),
        "file_path": pdf_path
    }

    supabase.table("pdf_files").insert(data).execute()