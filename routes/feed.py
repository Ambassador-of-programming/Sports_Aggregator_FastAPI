from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db


# Маршруты для ленты новостей
feed_router = APIRouter()

@feed_router.post("/")
def create_feed_item(title: str, category_id: int, image_url: Optional[str] = None, is_interesting: bool = False, db: Session = Depends(get_db)):
    """
    Создает новый элемент ленты новостей.
    
    Параметры:
    - title (str): Заголовок элемента ленты (обязательный).
    - category_id (int): Идентификатор спортивной категории, к которой относится элемент (обязательный).
    - image_url (str): URL изображения для элемента ленты (опционально).
    - is_interesting (bool): Флаг, указывающий, помечен ли элемент как интересный (по умолчанию: False).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Созданный элемент ленты новостей.
    """
    return crud.create_feed_item(db=db, title=title, category_id=category_id, image_url=image_url, is_interesting=is_interesting)

@feed_router.get("/{feed_item_id}")
def read_feed_item(feed_item_id: int, db: Session = Depends(get_db)):
    """
    Получает элемент ленты новостей по его идентификатору.
    
    Параметры:
    - feed_item_id (int): Идентификатор элемента ленты.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Элемент ленты новостей.
    
    Исключения:
    - HTTPException (status_code=404): Если элемент ленты не найден.
    """
    db_item = crud.get_feed_item(db, feed_item_id=feed_item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Элемент ленты не найден")
    return db_item

@feed_router.get("/")
def read_feed_items(skip: int = 0, limit: int = 100, category_id: Optional[int] = None, is_interesting: Optional[bool] = None, db: Session = Depends(get_db)):
    """
    Получает список элементов ленты новостей с пагинацией и фильтрацией.
    
    Параметры:
    - skip (int): Количество элементов, которые нужно пропустить (по умолчанию: 0).
    - limit (int): Максимальное количество элементов, которые нужно вернуть (по умолчанию: 100).
    - category_id (int): Фильтр по идентификатору спортивной категории (опционально).
    - is_interesting (bool): Фильтр по флагу "интересный" (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Список элементов ленты новостей.
    """
    items = crud.get_feed_items(db, skip=skip, limit=limit, category_id=category_id, is_interesting=is_interesting)
    return items

@feed_router.put("/{feed_item_id}")
def update_feed_item(feed_item_id: int, title: Optional[str] = None, category_id: Optional[int] = None, image_url: Optional[str] = None, is_interesting: Optional[bool] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные элемента ленты новостей.
    
    Параметры:
    - feed_item_id (int): Идентификатор элемента ленты.
    - title (str): Новый заголовок элемента (опционально).
    - category_id (int): Новый идентификатор спортивной категории (опционально).
    - image_url (str): Новый URL изображения элемента (опционально).
    - is_interesting (bool): Новый флаг "интересный" (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Обновленный элемент ленты новостей.
    
    Исключения:
    - HTTPException (status_code=404): Если элемент ленты не найден.
    """
    item_data = {}
    if title is not None:
        item_data["title"] = title
    if category_id is not None:  
        item_data["category_id"] = category_id
    if image_url is not None:
        item_data["image_url"] = image_url
    if is_interesting is not None:
        item_data["is_interesting"] = is_interesting
    
    updated_item = crud.update_feed_item(db, feed_item_id=feed_item_id, data=item_data)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Элемент ленты не найден")
    return updated_item

@feed_router.delete("/{feed_item_id}")
def delete_feed_item(feed_item_id: int, db: Session = Depends(get_db)):
    """
    Удаляет элемент ленты новостей.
    
    Параметры:
    - feed_item_id (int): Идентификатор элемента ленты.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если элемент ленты успешно удален, иначе False.
    """
    success = crud.delete_feed_item(db, feed_item_id=feed_item_id)
    return {"success": success}

@feed_router.post("/{feed_item_id}/like")
def like_feed_item(feed_item_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Добавляет лайк к элементу ленты новостей от пользователя.
    
    Параметры:
    - feed_item_id (int): Идентификатор элемента ленты.
    - user_id (int): Идентификатор пользователя, который ставит лайк.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Объект лайка.
    """
    like = crud.like_feed_item(db, feed_item_id=feed_item_id, user_id=user_id)
    return like

@feed_router.delete("/{feed_item_id}/like")
def unlike_feed_item(feed_item_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет лайк пользователя от элемента ленты новостей.
    
    Параметры:
    - feed_item_id (int): Идентификатор элемента ленты.
    - user_id (int): Идентификатор пользователя, который удаляет лайк.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если лайк успешно удален, иначе False.
    """
    success = crud.unlike_feed_item(db, feed_item_id=feed_item_id, user_id=user_id)
    return {"success": success}
  
@feed_router.post("/{feed_item_id}/views/increment")
def increment_feed_item_views(feed_item_id: int, db: Session = Depends(get_db)):
    """
    Увеличивает счетчик просмотров элемента ленты новостей.
    
    Параметры:
    - feed_item_id (int): Идентификатор элемента ленты.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если счетчик успешно увеличен, иначе False.
    """
    success = crud.increment_feed_item_views(db, feed_item_id=feed_item_id)
    return {"success": success}