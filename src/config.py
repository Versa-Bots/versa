import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]

DB_PATH = Path(os.getenv("DB_PATH") or Path("data/database.db")).absolute()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

HEALTHCHECK_HOST = os.getenv("HEALTHCHECK_HOST")
HEALTHCHECK_PORT_RAW = os.getenv("HEALTHCHECK_PORT")
HEALTHCHECK_PORT = int(HEALTHCHECK_PORT_RAW) if HEALTHCHECK_PORT_RAW else None
