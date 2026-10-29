from functools import lru_cache
from uuid import UUID

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings (BaseSettings):
    database_url :  str
    demo_organization_id : UUID
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="NEUROVIANS_",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()