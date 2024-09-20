from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine



BASE_DIR = Path(__file__).parent.parent.parent
DB_URL = f"sqlite+aiosqlite:///{BASE_DIR}/JuliaBars.sqlite3"

engine = create_async_engine(DB_URL, echo=True)