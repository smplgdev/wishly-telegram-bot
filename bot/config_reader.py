from pydantic import SecretStr, BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = Settings()
