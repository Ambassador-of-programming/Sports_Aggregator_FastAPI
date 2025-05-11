from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db

# Маршруты для спортивных категорий
sport_category_router = APIRouter()

@sport_category_router.post("/")
def create_sport_category(name: str, icon_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Создает новую спортивную категорию.

    - **name**: Название категории (обязательное).
    - **icon_url**: URL иконки категории (опционально).
    - **db**: Сессия базы данных.
    - Возвращает созданную спортивную категорию.
    """
    return crud.create_sport_category(db=db, name=name, icon_url=icon_url)

@sport_category_router.get("/{category_id}")
def read_sport_category(category_id: int, db: Session = Depends(get_db)):
    """
    Получает спортивную категорию по ее идентификатору.

    - **category_id**: Идентификатор спортивной категории.
    - **db**: Сессия базы данных.
    - Возвращает спортивную категорию.
    - Если спортивная категория не найдена, возвращает ошибку 404 Not Found.
    """
    db_category = crud.get_sport_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Спортивная категория не найдена")
    return db_category

@sport_category_router.get("/")
def read_sport_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получает список спортивных категорий с пагинацией.

    - **skip**: Количество категорий, которые нужно пропустить (по умолчанию 0).
    - **limit**: Максимальное количество категорий, которые нужно вернуть (по умолчанию 100).
    - **db**: Сессия базы данных.
    - Возвращает список спортивных категорий.
    """
    categories = crud.get_sport_categories(db, skip=skip, limit=limit)
    return categories

@sport_category_router.put("/{category_id}")
def update_sport_category(category_id: int, name: Optional[str] = None, icon_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные спортивной категории.

    - **category_id**: Идентификатор спортивной категории.
    - **name**: Новое название категории (опционально).
    - **icon_url**: Новый URL иконки категории (опционально).
    - **db**: Сессия базы данных.
    - Возвращает обновленную спортивную категорию.
    - Если спортивная категория не найдена, возвращает ошибку 404 Not Found.
    """
    category_data = {}
    if name is not None:
        category_data["name"] = name
    if icon_url is not None:
        category_data["icon_url"] = icon_url
    
    updated_category = crud.update_sport_category(db, category_id=category_id, data=category_data)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Спортивная категория не найдена")
    return updated_category

@sport_category_router.delete("/{category_id}")
def delete_sport_category(category_id: int, db: Session = Depends(get_db)):
    """
    Удаляет спортивную категорию.

    - **category_id**: Идентификатор спортивной категории.
    - **db**: Сессия базы данных.
    - Возвращает True, если спортивная категория успешно удалена, иначе False.
    """
    success = crud.delete_sport_category(db, category_id=category_id)
    return {"success": success}