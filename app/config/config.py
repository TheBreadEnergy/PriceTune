from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(CURRENT_DIR.parent.parent / "envs/.env"))

    DEBUG: bool = Field(False, env="DEBUG")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALLOWED_HOSTS: list[str] = Field(default=["localhost"], env="ALLOWED_HOSTS")

    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_PORT: str = Field(5432, env="DB_PORT")


settings = Settings()
