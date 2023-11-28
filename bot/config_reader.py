from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    BOT_USERNAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = "./.env"
        env_file_encoding = 'utf-8'


config = Settings()

DB_URI = f'postgresql+asyncpg://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_DATABASE}'
