from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс для настроек проекта, хранения и валидации переменных окружения."""

    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    REDIS_PORT: str
    REDIS_HOST: str
    WEB_PORT: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
    f"{settings.DB_HOST}:5432/{settings.DB_NAME}"
)

REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
