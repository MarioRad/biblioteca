import hashlib
from db.supabase_client import supabase

def upload_cover(file_bytes, pdf_path):
    file_hash = hashlib.md5(pdf_path.encode()).hexdigest()
    path = f"{file_hash}.jpg"

    try:
        supabase.storage.from_("covers").upload(
            path,
            file_bytes,
            {
            "content-type": "image/jpeg",
            "upsert": "true"
            }
        )
    except Exception as e:
        print("Error subiendo portada:", e)
        url = f"{supabase.supabase_url}/storage/v1/object/public/covers/{path}"
        return url