from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    environment: str = "development"

    oci_tenancy: str
    oci_user: str
    oci_fingerprint: str
    oci_private_key: str
    oci_region: str
    oci_namespace: str
    oci_bucket_name: str

    class Config:
        env_file = ".env"

settings = Settings()