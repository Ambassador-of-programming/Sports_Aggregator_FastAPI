from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db

# Маршруты для пользователей
user_router = APIRouter()

@user_router.post("/")
def create_user(username: str, password: str, avatar_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Создает нового пользователя.

    - **username**: Имя пользователя (обязательное).
    - **avatar_url**: URL аватара пользователя (опционально).
    - **db**: Сессия базы данных.
    - Возвращает созданного пользователя.
    - Если имя пользователя уже занято, возвращает ошибку 400 Bad Request.
    """
    db_user = crud.get_user_by_username(db, username=username, password=password)
    if db_user:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
    return crud.create_user(db=db, username=username, password=password, avatar_url=avatar_url)

@user_router.get("/{username}")
def read_user(username: str, password: str,  db: Session = Depends(get_db)):
    """
    Получает пользователя по его идентификатору.

    - **username**: Идентификатор пользователя.
    - **db**: Сессия базы данных.
    - Возвращает пользователя.
    - Если пользователь не найден, возвращает ошибку 404 Not Found.
    """
    db_user = crud.get_user_by_username(db, username=username, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@user_router.get("/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получает список пользователей с пагинацией.

    - **skip**: Количество пользователей, которые нужно пропустить (по умолчанию 0).
    - **limit**: Максимальное количество пользователей, которые нужно вернуть (по умолчанию 100).
    - **db**: Сессия базы данных.
    - Возвращает список пользователей.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@user_router.put("/{user_id}")
def update_user(user_id: int, username: Optional[str] = None, avatar_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные пользователя.

    - **user_id**: Идентификатор пользователя.
    - **username**: Новое имя пользователя (опционально).
    - **avatar_url**: Новый URL аватара пользователя (опционально).
    - **db**: Сессия базы данных.
    - Возвращает обновленного пользователя.
    - Если пользователь не найден, возвращает ошибку 404 Not Found.
    """
    user_data = {}
    if username is not None:
        user_data["username"] = username
    if avatar_url is not None:
        user_data["avatar_url"] = avatar_url
    
    updated_user = crud.update_user(db, user_id=user_id, data=user_data)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user

@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет пользователя.

    - **user_id**: Идентификатор пользователя.
    - **db**: Сессия базы данных.
    - Возвращает True, если пользователь успешно удален, иначе False.
    """
    success = crud.delete_user(db, user_id=user_id)
    return {"success": success}

@user_router.post("/{user_id}/followers/increment")
def increment_user_followers(user_id: int, db: Session = Depends(get_db)):
    """
    Увеличивает счетчик подписчиков пользователя.

    - **user_id**: Идентификатор пользователя.
    - **db**: Сессия базы данных.
    - Возвращает True, если счетчик успешно увеличен, иначе False.
    """
    success = crud.increment_user_followers(db, user_id=user_id)
    return {"success": success}

@user_router.post("/{user_id}/followers/decrement")
def decrement_user_followers(user_id: int, db: Session = Depends(get_db)):
    """
    Уменьшает счетчик подписчиков пользователя.

    - **user_id**: Идентификатор пользователя.
    - **db**: Сессия базы данных.
    - Возвращает True, если счетчик успешно уменьшен, иначе False.
    """
    success = crud.decrement_user_followers(db, user_id=user_id)
    return {"success": success}

@user_router.post("/{user_id}/reviews/increment")
def increment_user_reviews(user_id: int, db: Session = Depends(get_db)):
    """
    Увеличивает счетчик отзывов пользователя.

    - **user_id**: Идентификатор пользователя.
    - **db**: Сессия базы данных.
    - Возвращает True, если счетчик успешно увеличен, иначе False.
    """
    success = crud.increment_user_reviews(db, user_id=user_id)
    return {"success": success}