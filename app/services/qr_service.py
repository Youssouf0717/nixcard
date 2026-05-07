import os
import io
import qrcode
import cloudinary
import cloudinary.uploader


def _configured() -> bool:
    return bool(os.getenv("CLOUDINARY_CLOUD_NAME"))


def _setup():
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )


def generate_qr(slug: str) -> str:
    base_url = os.getenv("BASE_URL", "http://localhost:5000")
    url = f"{base_url}/card/{slug}"

    img = qrcode.make(url)

    if _configured():
        _setup()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        result = cloudinary.uploader.upload(
            buf,
            public_id=f"nixcard/qr/{slug}",
            overwrite=True,
            resource_type="image",
        )
        return result["secure_url"]

    # Fallback local
    folder = os.path.join("app", "static", "qr")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{slug}.png")
    img.save(path)
    return f"qr/{slug}.png"


def delete_qr(slug: str) -> None:
    if _configured():
        _setup()
        cloudinary.uploader.destroy(f"nixcard/qr/{slug}", resource_type="image")
        return
    path = os.path.join("app", "static", "qr", f"{slug}.png")
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
