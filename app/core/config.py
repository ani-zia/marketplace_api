from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Marketplace API"
    database_url: str
    secret: str = "SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
