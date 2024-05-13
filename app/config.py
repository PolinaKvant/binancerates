from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    DB_URL: str
    DB_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

settings = Settings()

