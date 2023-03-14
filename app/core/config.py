from pydantic import BaseSettings

from app.core.constants import PAGINATION_DEFAULT, PASSWORD_MIN_LENGHT


class Settings(BaseSettings):
    app_title: str = "Marketplace API"
    database_url: str
    database_test_url: str
    secret: str = "SECRET"
    password_min_length: int = PASSWORD_MIN_LENGHT
    pagination_default: int = PAGINATION_DEFAULT

    class Config:
        env_file = ".env"


settings = Settings()
