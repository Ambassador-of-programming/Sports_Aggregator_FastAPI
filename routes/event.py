from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db
from fastapi import Query


# Маршруты для мероприятий
event_router = APIRouter()

@event_router.get("/check_user")
def check_user_events(user_id: int, db: Session = Depends(get_db)):
    """
    Проверка есть ли у пользователя мероприятия.

    - **user_id**: Идентификатор пользователя, который регистрируется на мероприятие.
    - **db**: Сессия базы данных.
    - Возвращает объект меропрития пользователя.
.
    """
    registration = crud.check_event_user(db, user_id=user_id)
    if registration is None:
        raise HTTPException(status_code=400, detail="Пользователь не зарегистрирован на мероприятие.")
    return registration


@event_router.post("/")
def create_event(title: str, description: str, sport_category_id: int, event_date: datetime, 
                 image_url: Optional[str] = None,
                 registration_end_date: Optional[datetime] = None, price: float = 0, 
                 available_seats: int = 0, total_seats: int = 0, location: Optional[str] = None, 
                 longitude: Optional[float] = None, latitude: Optional[float] = None, 
                 competition_rules: Optional[str] = None, owner_id: Optional[int] = None, 
                 status: str = "new", db: Session = Depends(get_db)):
    """
    Создает новое мероприятие.

    - **title**: Название мероприятия (обязательное).
    - **description**: Описание мероприятия (обязательное).
    - **image_url**: URL изображения мероприятия (опционально).
    - **sport_category_id**: Идентификатор спортивной категории (обязательный).
    - **event_date**: Дата проведения мероприятия (обязательная).
    - **registration_end_date**: Дата окончания регистрации (опционально).
    - **price**: Цена мероприятия (по умолчанию 0).
    - **available_seats**: Количество доступных мест (по умолчанию 0).
    - **total_seats**: Общее количество мест (по умолчанию 0).
    - **location**: Место проведения мероприятия (опционально).
    - **longitude**: Долгота места проведения (опционально).
    - **latitude**: Широта места проведения (опционально).
    - **competition_rules**: Правила соревнований (опционально).
    - **owner_id**: Идентификатор владельца мероприятия (опционально).
    - **status**: Статус мероприятия (по умолчанию "new").
    - **db**: Сессия базы данных.
    - Возвращает созданное мероприятие.
    """
    event_data = {
        "title": title,
        "description": description,
        "image_url": image_url,
        "sport_category_id": sport_category_id,
        "event_date": event_date,
        "registration_end_date": registration_end_date,
        "price": price,
        "available_seats": available_seats,
        "total_seats": total_seats,
        "location": location,
        "longitude": longitude,
        "latitude": latitude,
        "competition_rules": competition_rules,
        "owner_id": owner_id,
        "status": status
    }
    return crud.create_event(db=db, data=event_data)

@event_router.get("/{event_id}")
def read_event(event_id: int, db: Session = Depends(get_db)):
    """
    Получает мероприятие по его идентификатору.

    - **event_id**: Идентификатор мероприятия.
    - **db**: Сессия базы данных.
    - Возвращает мероприятие.
    - Если мероприятие не найдено, возвращает ошибку 404 Not Found.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    return db_event

@event_router.get("/")
def read_events(skip: int = 0, limit: int = 100, category_id: Optional[int] = None, 
                status: Optional[str] = None, owner_id: Optional[int] = None, 
                min_date: Optional[datetime] = None, max_date: Optional[datetime] = None, 
                latitude: Optional[float] = None, longitude: Optional[float] = None, 
                distance: Optional[float] = None, db: Session = Depends(get_db)):
    """
    Получает список мероприятий с пагинацией и фильтрацией.

    - **skip**: Количество мероприятий, которые нужно пропустить (по умолчанию 0).
    - **limit**: Максимальное количество мероприятий, которые нужно вернуть (по умолчанию 100).
    - **category_id**: Фильтр по идентификатору спортивной категории (опционально).
    - **status**: Фильтр по статусу мероприятия (опционально).
    - **owner_id**: Фильтр по идентификатору владельца мероприятия (опционально).
    - **min_date**: Фильтр по минимальной дате проведения мероприятия (опционально).
    - **max_date**: Фильтр по максимальной дате проведения мероприятия (опционально).
    - **latitude**: Фильтр по широте места проведения (опционально).
    - **longitude**: Фильтр по долготе места проведения (опционально).
    - **distance**: Фильтр по расстоянию от указанных координат (опционально).
    - **db**: Сессия базы данных.
    - Возвращает список мероприятий.
    """
    events = crud.get_events(db, skip=skip, limit=limit, category_id=category_id, status=status, 
                             owner_id=owner_id, min_date=min_date, max_date=max_date, 
                             latitude=latitude, longitude=longitude, distance=distance)
    return events

@event_router.put("/{event_id}")
def update_event(event_id: int, title: Optional[str] = None, description: Optional[str] = None,
                 image_url: Optional[str] = None, 
                 sport_category_id: Optional[int] = None, event_date: Optional[datetime] = None, 
                 registration_end_date: Optional[datetime] = None, price: Optional[float] = None, 
                 available_seats: Optional[int] = None, total_seats: Optional[int] = None, 
                 location: Optional[str] = None, longitude: Optional[float] = None, 
                 latitude: Optional[float] = None, competition_rules: Optional[str] = None, 
                 owner_id: Optional[int] = None, status: Optional[str] = None, 
                 db: Session = Depends(get_db)):
    """
    Обновляет данные мероприятия.

    - **event_id**: Идентификатор мероприятия.
    - **title**: Новое название мероприятия (опционально).
    - **description**: Новое описание мероприятия (опционально).
    - **image_url**: Новый URL изображения мероприятия (опционально).
    - **sport_category_id**: Новый идентификатор спортивной категории (опционально).
    - **event_date**: Новая дата проведения мероприятия (опционально).
    - **registration_end_date**: Новая дата окончания регистрации (опционально).
    - **price**: Новая цена мероприятия (опционально).
    - **available_seats**: Новое количество доступных мест (опционально).
    - **total_seats**: Новое общее количество мест (опционально).
    - **location**: Новое место проведения мероприятия (опционально).
    - **longitude**: Новая долгота места проведения (опционально).
    - **latitude**: Новая широта места проведения (опционально).
    - **competition_rules**: Новые правила соревнований (опционально).
    - **owner_id**: Новый идентификатор владельца мероприятия (опционально).
    - **status**: Новый статус мероприятия (опционально).
    - **db**: Сессия базы данных.
    - Возвращает обновленное мероприятие.
    - Если мероприятие не найдено, возвращает ошибку 404 Not Found.
    """
    event_data = {}
    if title is not None:
        event_data["title"] = title
    if description is not None:
        event_data["description"] = description
    if image_url is not None:
        event_data["image_url"] = image_url
    if sport_category_id is not None:
        event_data["sport_category_id"] = sport_category_id
    if event_date is not None:
        event_data["event_date"] = event_date
    if registration_end_date is not None:
        event_data["registration_end_date"] = registration_end_date
    if price is not None:
        event_data["price"] = price
    if available_seats is not None:
        event_data["available_seats"] = available_seats
    if total_seats is not None:
        event_data["total_seats"] = total_seats
    if location is not None:
        event_data["location"] = location
    if longitude is not None:
        event_data["longitude"] = longitude
    if latitude is not None:
        event_data["latitude"] = latitude
    if competition_rules is not None:
        event_data["competition_rules"] = competition_rules
    if owner_id is not None:
        event_data["owner_id"] = owner_id
    if status is not None:
        event_data["status"] = status
    
    updated_event = crud.update_event(db, event_id=event_id, data=event_data)
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    return updated_event

@event_router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Удаляет мероприятие.

    - **event_id**: Идентификатор мероприятия.
    - **db**: Сессия базы данных.
    - Возвращает True, если мероприятие успешно удалено, иначе False.
    """
    success = crud.delete_event(db, event_id=event_id)
    return {"success": success}

@event_router.post("/{event_id}/like")
def like_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Добавляет лайк к мероприятию от пользователя.

    - **event_id**: Идентификатор мероприятия.
    - **user_id**: Идентификатор пользователя, который ставит лайк.
    - **db**: Сессия базы данных.
    - Возвращает объект лайка.
    """
    like = crud.like_event(db, event_id=event_id, user_id=user_id)
    return like

@event_router.delete("/{event_id}/like")
def unlike_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет лайк пользователя от мероприятия.

    - **event_id**: Идентификатор мероприятия.
    - **user_id**: Идентификатор пользователя, который удаляет лайк.
    - **db**: Сессия базы данных.
    - Возвращает True, если лайк успешно удален, иначе False.
    """
    success = crud.unlike_event(db, event_id=event_id, user_id=user_id)
    return {"success": success}

@event_router.post("/{event_id}/views/increment")
def increment_event_views(event_id: int, db: Session = Depends(get_db)):
    """
    Увеличивает счетчик просмотров мероприятия.

    - **event_id**: Идентификатор мероприятия.
    - **db**: Сессия базы данных.
    - Возвращает True, если счетчик успешно увеличен, иначе False.
    """
    success = crud.increment_event_views(db, event_id=event_id)
    return {"success": success}

@event_router.post("/{event_id}/register")
def register_for_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Регистрирует пользователя на мероприятие.

    - **event_id**: Идентификатор мероприятия.
    - **user_id**: Идентификатор пользователя, который регистрируется на мероприятие.
    - **db**: Сессия базы данных.
    - Возвращает объект регистрации.
    - Если регистрация не удалась (нет свободных мест), возвращает ошибку 400 Bad Request.
    """
    registration = crud.register_for_event(db, event_id=event_id, user_id=user_id)
    if registration is None:
        raise HTTPException(status_code=400, detail="Регистрация не удалась. Нет свободных мест.")
    return registration

