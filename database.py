# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # sólo para desarrollo local; no subir .env con secrets

# Preferir DATABASE_URL (Render) — si no existe, construir desde variables sueltas (local)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "fantasy")
    DB_PASS = os.getenv("DB_PASS", "fantasy123")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "fantasydb")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine con pool_pre_ping para evitar conexiones muertas
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# sessionmaker y Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
