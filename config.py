import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    _database_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/roda")
    if _database_url and _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    TASA_INTERES_ANUAL = float(os.getenv("TASA_INTERES_ANUAL", "0.144"))
