from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = ("Number Guessing Game",)
    items_per_user: int = 50


@lru_cache
def get_settings():
    return Settings()
