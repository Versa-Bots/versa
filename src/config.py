import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]

DB_PATH = Path(os.getenv("DB_PATH") or Path("data/database.db")).absolute()
