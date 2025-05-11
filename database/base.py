from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Создаем базовый класс для моделей
Base = declarative_base()

# # Создаем URL для подключения к PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost:5432/postgres"

# Создаем URL для подключения к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres:5432/database"

# Создаем движок базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Создаем класс сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()