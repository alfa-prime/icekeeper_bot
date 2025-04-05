from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс конфигурации приложения.
    Использует `pydantic.BaseSettings` для автоматической загрузки переменных окружения
    и их валидации.
    """
    ADMIN_ID: int
    BOT_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",  # Автоматически загружает переменные из .env
        env_file_encoding="utf-8",  # Поддержка UTF-8
        extra="ignore",  # Игнорирует неизвестные переменные окружения из .env
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Получает объект конфигурации с кэшированием.
    Использует `lru_cache()`, чтобы загружать настройки только **один раз** при запуске приложения.
    """
    return Settings()
