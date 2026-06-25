from fastapi import APIRouter, UploadFile

from app.schemas.image import ImageUploadResponse
from app.services.storage_service import upload_image

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image_route(file: UploadFile):
    file_bytes = await file.read()
    object_name = upload_image(file_bytes, file.filename or "image.jpg")
    return ImageUploadResponse(object_name=object_name)
