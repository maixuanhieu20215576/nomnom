from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    object_name: str
