from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db


# Маршруты для спортивных площадок
venue_router = APIRouter()

@venue_router.post("/")
def create_venue(name: str, address: str, owner_id: int, venue_type: str, sport_category_id: int, description: Optional[str] = None, image_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Создает новую спортивную площадку.
    
    Параметры:
    - name (str): Название площадки (обязательный).
    - address (str): Адрес площадки (обязательный).
    - owner_id (int): Идентификатор владельца площадки (обязательный).
    - venue_type (str): Тип площадки (обязательный).
    - sport_category_id (int): Идентификатор спортивной категории (обязательный).
    - description (str): Описание площадки (опционально).
    - image_url (str): URL изображения площадки (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Созданную спортивную площадку.
    """
    venue_data = {
        "name": name,
        "address": address,
        "owner_id": owner_id,
        "venue_type": venue_type,
        "sport_category_id": sport_category_id,
        "description": description,
        "image_url": image_url
    }
    return crud.create_venue(db=db, data=venue_data)

@venue_router.get("/{venue_id}")
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    """
    Получает спортивную площадку по ее идентификатору.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Спортивную площадку.
    
    Исключения:
    - HTTPException (status_code=404): Если спортивная площадка не найдена.
    """
    db_venue = crud.get_venue(db, venue_id=venue_id)
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Спортивная площадка не найдена")
    return db_venue

@venue_router.get("/")
def read_venues(skip: int = 0, limit: int = 100, category_id: Optional[int] = None, venue_type: Optional[str] = None, owner_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Получает список спортивных площадок с пагинацией и фильтрацией.
    
    Параметры:
    - skip (int): Количество площадок, которые нужно пропустить (по умолчанию: 0).
    - limit (int): Максимальное количество площадок, которые нужно вернуть (по умолчанию: 100).
    - category_id (int): Фильтр по идентификатору спортивной категории (опционально).
    - venue_type (str): Фильтр по типу площадки (опционально).
    - owner_id (int): Фильтр по идентификатору владельца площадки (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Список спортивных площадок.
    """
    venues = crud.get_venues(db, skip=skip, limit=limit, category_id=category_id, venue_type=venue_type, owner_id=owner_id)
    return venues

@venue_router.put("/{venue_id}")
def update_venue(venue_id: int, name: Optional[str] = None, address: Optional[str] = None, owner_id: Optional[int] = None, venue_type: Optional[str] = None, sport_category_id: Optional[int] = None, description: Optional[str] = None, image_url: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные спортивной площадки.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - name (str): Новое название площадки (опционально).
    - address (str): Новый адрес площадки (опционально).
    - owner_id (int): Новый идентификатор владельца площадки (опционально).
    - venue_type (str): Новый тип площадки (опционально).
    - sport_category_id (int): Новый идентификатор спортивной категории (опционально).
    - description (str): Новое описание площадки (опционально).
    - image_url (str): Новый URL изображения площадки (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Обновленную спортивную площадку.
    
    Исключения:
    - HTTPException (status_code=404): Если спортивная площадка не найдена.
    """
    venue_data = {}
    if name is not None:
        venue_data["name"] = name
    if address is not None:
        venue_data["address"] = address
    if owner_id is not None:
        venue_data["owner_id"] = owner_id
    if venue_type is not None:
        venue_data["venue_type"] = venue_type
    if sport_category_id is not None:
        venue_data["sport_category_id"] = sport_category_id
    if description is not None:
        venue_data["description"] = description
    if image_url is not None:
        venue_data["image_url"] = image_url
    
    updated_venue = crud.update_venue(db, venue_id=venue_id, data=venue_data)
    if updated_venue is None:
        raise HTTPException(status_code=404, detail="Спортивная площадка не найдена")
    return updated_venue

@venue_router.delete("/{venue_id}")
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    """
    Удаляет спортивную площадку.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если спортивная площадка успешно удалена, иначе False.
    """
    success = crud.delete_venue(db, venue_id=venue_id)
    return {"success": success}

@venue_router.post("/{venue_id}/like")
def like_venue(venue_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Добавляет лайк к спортивной площадке от пользователя.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - user_id (int): Идентификатор пользователя, который ставит лайк.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Объект лайка.
    """
    like = crud.like_venue(db, venue_id=venue_id, user_id=user_id)
    return like

@venue_router.delete("/{venue_id}/like")
def unlike_venue(venue_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет лайк пользователя от спортивной площадки.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - user_id (int): Идентификатор пользователя, который удаляет лайк.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если лайк успешно удален, иначе False.
    """
    success = crud.unlike_venue(db, venue_id=venue_id, user_id=user_id)
    return {"success": success}

@venue_router.post("/{venue_id}/time-slots")
def create_time_slot(venue_id: int, start_time: datetime, end_time: datetime, date: Optional[datetime] = None, is_available: bool = True, db: Session = Depends(get_db)):
    """
    Создает временной слот для спортивной площадки.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - start_time (datetime): Время начала слота.
    - end_time (datetime): Время окончания слота.
    - date (datetime): Дата слота (опционально, по умолчанию: дата из start_time).
    - is_available (bool): Флаг доступности слота (по умолчанию: True).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Созданный временной слот.
    """
    time_slot = crud.create_time_slot(db, venue_id=venue_id, start_time=start_time, end_time=end_time, date=date, is_available=is_available)
    return time_slot

@venue_router.get("/{venue_id}/time-slots")
def read_venue_time_slots(venue_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, is_available: Optional[bool] = None, db: Session = Depends(get_db)):
    """
    Получает временные слоты для спортивной площадки с фильтрацией.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - start_date (datetime): Фильтр по начальной дате слотов (опционально).
    - end_date (datetime): Фильтр по конечной дате слотов (опционально).
    - is_available (bool): Фильтр по доступности слотов (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Список временных слотов.
    """
    time_slots = crud.get_venue_time_slots(db, venue_id=venue_id, start_date=start_date, end_date=end_date, is_available=is_available)
    return time_slots

@venue_router.put("/time-slots/{time_slot_id}")
def update_time_slot(time_slot_id: int, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, date: Optional[datetime] = None, is_available: Optional[bool] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные временного слота.
    
    Параметры:
    - time_slot_id (int): Идентификатор временного слота.
    - start_time (datetime): Новое время начала слота (опционально).
    - end_time (datetime): Новое время окончания слота (опционально).
    - date (datetime): Новая дата слота (опционально).
    - is_available (bool): Новый флаг доступности слота (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Обновленный временной слот.
    - Если временной слот не найден, возвращает None.
    """
    time_slot_data = {}
    if start_time is not None:
        time_slot_data["start_time"] = start_time
    if end_time is not None:
        time_slot_data["end_time"] = end_time
    if date is not None:
        time_slot_data["date"] = date
    if is_available is not None:
        time_slot_data["is_available"] = is_available
    
    updated_time_slot = crud.update_time_slot(db, time_slot_id=time_slot_id, data=time_slot_data)
    return updated_time_slot

@venue_router.delete("/time-slots/{time_slot_id}")
def delete_time_slot(time_slot_id: int, db: Session = Depends(get_db)):
    """
    Удаляет временной слот.
    
    Параметры:
    - time_slot_id (int): Идентификатор временного слота.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если временной слот успешно удален, иначе False.
    """
    success = crud.delete_time_slot(db, time_slot_id=time_slot_id)
    return {"success": success}

@venue_router.post("/{venue_id}/services")
def create_venue_service(venue_id: int, name: str, price: float, description: Optional[str] = None, is_active: bool = True, db: Session = Depends(get_db)):
    """
    Создает услугу для спортивной площадки.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - name (str): Название услуги (обязательный).
    - price (float): Цена услуги (обязательный).
    - description (str): Описание услуги (опционально).
    - is_active (bool): Флаг активности услуги (по умолчанию: True).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Созданную услугу.
    """
    return crud.create_venue_service(db, venue_id=venue_id, name=name, price=price, description=description, is_active=is_active)

@venue_router.get("/{venue_id}/services")
def read_venue_services(venue_id: int, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    """
    Получает услуги для спортивной площадки с фильтрацией.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - is_active (bool): Фильтр по активности услуг (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Список услуг.
    """
    services = crud.get_venue_services(db, venue_id=venue_id, is_active=is_active)
    return services

@venue_router.put("/services/{service_id}")
def update_venue_service(service_id: int, name: Optional[str] = None, price: Optional[float] = None, description: Optional[str] = None, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
   """
   Обновляет данные услуги спортивной площадки.
   
   Параметры:
   - service_id (int): Идентификатор услуги.
   - name (str): Новое название услуги (опционально).
   - price (float): Новая цена услуги (опционально).
   - description (str): Новое описание услуги (опционально).
   - is_active (bool): Новый флаг активности услуги (опционально).
   - db (Session): Сессия базы данных.
   
   Возвращает:
   - Обновленную услугу.
   - Если услуга не найдена, возвращает None.
   """
   service_data = {}
   if name is not None:
       service_data["name"] = name
   if price is not None:
       service_data["price"] = price
   if description is not None:
       service_data["description"] = description
   if is_active is not None:
       service_data["is_active"] = is_active
   
   updated_service = crud.update_venue_service(db, service_id=service_id, data=service_data)
   return updated_service

@venue_router.delete("/services/{service_id}")
def delete_venue_service(service_id: int, db: Session = Depends(get_db)):
   """
   Удаляет услугу спортивной площадки.
   
   Параметры:
   - service_id (int): Идентификатор услуги.
   - db (Session): Сессия базы данных.
   
   Возвращает:
   - Словарь с ключом "success" и значением True, если услуга успешно удалена, иначе False.
   """
   success = crud.delete_venue_service(db, service_id=service_id)
   return {"success": success}