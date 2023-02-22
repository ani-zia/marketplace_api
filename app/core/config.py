from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str

    class Config:
        env_file = ".env"


settings = Settings()
