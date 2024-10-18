from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "JuliaBars.sqlite3"

class Settings(BaseSettings):
    
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    
        
    private_key: Path = BASE_DIR / "app" / "authentication" / "certs" / "jwt-private.pem"    
    public_key: Path = BASE_DIR / "app" / "authentication" / "certs" / "jwt-public.pem"
 
    algorithm: str = "RS256"
    access_token_expire_minute: int = 30
    access_token_refresh_days: int = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

