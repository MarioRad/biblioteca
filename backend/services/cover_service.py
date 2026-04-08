import requests
from services.storage_service import upload_cover
from PIL import Image, ImageDraw
import io

def download_image(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.content
    except:
        return None


def get_book_cover(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    r = requests.get(url).json()

    if "items" in r:
        info = r["items"][0]["volumeInfo"]
        return info.get("imageLinks", {}).get("thumbnail")

    return None


def search_by_title(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    r = requests.get(url).json()

    if "items" in r:
        info = r["items"][0]["volumeInfo"]
        return info.get("imageLinks", {}).get("thumbnail")

    return None


def generate_cover(title):
    title = str(title or "PDF")
    img = Image.new('RGB', (300, 450), color=(40, 40, 40))
    d = ImageDraw.Draw(img)

  # dividir en líneas
    lines = [title[i:i+20] for i in range(0, len(title), 20)]

    y = 180
    for line in lines[:3]:
        d.text((10, y), line, fill=(255,255,255))
        y += 20

    import io
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

"""     d.text((10, 200), title[:30], fill=(255,255,255))

    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue() """


def get_cover(meta, isbn, pdf_path):
    cover_url = None

    # 1. ISBN
    if isbn:
        cover_url = get_book_cover(isbn)

    # 2. fallback título
    if not cover_url and meta.get("title"):
        cover_url = search_by_title(meta["title"])

    # 3. descargar y subir
    if cover_url:
        img = download_image(cover_url)
        if img:
            return upload_cover(img, pdf_path)

    # 4. fallback final
    img = generate_cover(meta.get("title", "PDF"))
    return upload_cover(img, pdf_path)