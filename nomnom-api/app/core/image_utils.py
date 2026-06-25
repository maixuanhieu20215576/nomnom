import io

from PIL import Image

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024


def resize_image_to_max_size(image_bytes: bytes, max_size_bytes: int = MAX_IMAGE_SIZE_BYTES) -> bytes:
    if len(image_bytes) <= max_size_bytes:
        return image_bytes

    image = Image.open(io.BytesIO(image_bytes))
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    quality = 90
    while quality >= 20:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        if buffer.tell() <= max_size_bytes:
            return buffer.getvalue()
        quality -= 10

    while True:
        image = image.resize((image.width // 2, image.height // 2))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=70)
        if buffer.tell() <= max_size_bytes or min(image.width, image.height) < 50:
            return buffer.getvalue()
