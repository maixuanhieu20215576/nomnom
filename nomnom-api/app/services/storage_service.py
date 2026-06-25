import uuid
from functools import lru_cache

import oci

from app.core.config import settings
from app.core.image_utils import resize_image_to_max_size


@lru_cache(maxsize=1)
def _get_object_storage_client() -> oci.object_storage.ObjectStorageClient:
    config = {
        "tenancy": settings.oci_tenancy,
        "user": settings.oci_user,
        "fingerprint": settings.oci_fingerprint,
        "key_content": settings.oci_private_key,
        "region": settings.oci_region,
    }
    return oci.object_storage.ObjectStorageClient(config)


def _build_public_url(object_name: str) -> str:
    return (
        f"https://objectstorage.{settings.oci_region}.oraclecloud.com"
        f"/n/{settings.oci_namespace}/b/{settings.oci_bucket_name}/o/{object_name}"
    )


def upload_image(file_bytes: bytes, filename: str) -> str:
    resized_bytes = resize_image_to_max_size(file_bytes)

    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpg"
    object_name = f"{uuid.uuid4().hex}.{extension}"

    client = _get_object_storage_client()
    client.put_object(
        namespace_name=settings.oci_namespace,
        bucket_name=settings.oci_bucket_name,
        object_name=object_name,
        put_object_body=resized_bytes,
    )

    return _build_public_url(object_name)
