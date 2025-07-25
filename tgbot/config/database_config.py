from dotenv import dotenv_values
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'

config = dotenv_values(dotenv_path=env_path)

if config["DATABASE_URL"] is None:
	raise ValueError("Database URL is required in /tgbot/.env")

DATABASE_URL = config["DATABASE_URL"]