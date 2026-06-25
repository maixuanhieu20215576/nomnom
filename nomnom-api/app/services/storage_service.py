import mimetypes
import uuid
from functools import lru_cache

import boto3

from app.core.config import settings
from app.core.image_utils import resize_image_to_max_size

PRESIGNED_URL_EXPIRY_SECONDS = 3600


@lru_cache(maxsize=1)
def _get_object_storage_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.b2_endpoint_url,
        aws_access_key_id=settings.b2_key_id,
        aws_secret_access_key=settings.b2_application_key,
        region_name=settings.b2_region,
    )


def upload_image(file_bytes: bytes, filename: str) -> str:
    """Resizes and uploads the image, returning its object_name (not a URL).

    Persist the returned object_name (the bucket is private), then call
    get_image_url() to derive a presigned URL whenever the image needs to
    be served to a client.
    """
    resized_bytes = resize_image_to_max_size(file_bytes)

    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpg"
    object_name = f"{uuid.uuid4().hex}.{extension}"
    content_type = mimetypes.guess_type(object_name)[0] or "application/octet-stream"

    client = _get_object_storage_client()
    client.put_object(
        Bucket=settings.b2_bucket_name,
        Key=object_name,
        Body=resized_bytes,
        ContentType=content_type,
    )

    return object_name


def get_image_url(object_name: str, expires_in: int = PRESIGNED_URL_EXPIRY_SECONDS) -> str:
    client = _get_object_storage_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.b2_bucket_name, "Key": object_name},
        ExpiresIn=expires_in,
    )
