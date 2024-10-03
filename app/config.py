from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    @property
    def DB_URL(self):
        return "sqlite+aiosqlite:///JuliaBars.sqlite3"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()