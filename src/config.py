import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]

DB_PATH = Path(os.getenv("DB_PATH") or Path("data/database.db")).absolute()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

HEALTHCHECK_HOST = os.getenv("HEALTHCHECK_HOST", "127.0.0.1")
HEALTHCHECK_PORT = int(os.getenv("HEALTHCHECK_PORT", "8080"))
HEALTHCHECK_PATH = os.getenv("HEALTHCHECK_PATH", "/")

if not HEALTHCHECK_PATH.startswith("/"):
    HEALTHCHECK_PATH = f"/{HEALTHCHECK_PATH}"
