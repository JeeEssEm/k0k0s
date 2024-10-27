from io import BytesIO

from fastapi import UploadFile
from PIL import Image

from exceptions import ImageConvertingError, FileMustBeImage


async def convert_image_to_webp(image: UploadFile) -> BytesIO:
    if not image.content_type.startswith('image/'):
        raise FileMustBeImage

    try:
        image = Image.open(BytesIO(await image.read()))
    except Exception:
        raise ImageConvertingError

    output = BytesIO()
    try:
        image.save(output, 'WEBP', quality=70)
        output.seek(0)
    except Exception:
        raise ImageConvertingError
    return output
