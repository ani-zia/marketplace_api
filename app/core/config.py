from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Marketplace API"
    database_url: str
    secret: str = "SECRET"
    password_min_length: int = 3
    pagination_default: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
