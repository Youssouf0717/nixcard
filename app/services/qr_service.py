import os
import qrcode


def generate_qr(slug: str) -> str:
    base_url = os.getenv("BASE_URL", "http://localhost:5000")
    url = f"{base_url}/card/{slug}"
    folder = os.path.join("app", "static", "qr")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{slug}.png")
    if not os.path.exists(path):
        img = qrcode.make(url)
        img.save(path)
    return f"qr/{slug}.png"


def delete_qr(slug: str) -> None:
    path = os.path.join("app", "static", "qr", f"{slug}.png")
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
