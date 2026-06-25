from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    environment: str = "development"

    b2_endpoint_url: str
    b2_key_id: str
    b2_application_key: str
    b2_bucket_name: str
    b2_region: str

    class Config:
        env_file = ".env"

settings = Settings()