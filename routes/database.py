from fastapi import APIRouter
from database import Base, engine, create_tables


# Маршруты для ленты новостей
database_router = APIRouter()

@database_router.post("/")
def create_table():
    create_tables()
    return {"message": "Таблицы созданы"}
    
@database_router.post("/drop")
def drop_table():
    Base.metadata.drop_all(bind=engine)
    return {"message": "Таблицы удалены"}