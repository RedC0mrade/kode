from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = "sqlite+aisaqliteo///./joes_ticket.sqlite3"

settings = Settings()
