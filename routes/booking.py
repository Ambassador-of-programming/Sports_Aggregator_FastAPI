from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db


# Маршруты для бронирований
booking_router = APIRouter()

@booking_router.post("/")
def create_booking(user_id: int, venue_id: int, time_slot_id: int, db: Session = Depends(get_db)):
    """
    Создает бронирование спортивной площадки.
    
    Параметры:
    - user_id (int): Идентификатор пользователя.
    - venue_id (int): Идентификатор спортивной площадки.
    - time_slot_id (int): Идентификатор временного слота.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Созданное бронирование.
    - Если бронирование не удалось (временной слот занят), возвращает None.
    """
    booking = crud.create_booking(db, user_id=user_id, venue_id=venue_id, time_slot_id=time_slot_id)
    return booking

@booking_router.get("/{booking_id}")
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Получает бронирование по его идентификатору.
    
    Параметры:
    - booking_id (int): Идентификатор бронирования.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Бронирование.
    
    Исключения:
    - HTTPException (status_code=404): Если бронирование не найдено.
    """
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return db_booking

@booking_router.get("/users/{user_id}")
def read_user_bookings(user_id: int, status: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Получает бронирования пользователя с фильтрацией по статусу.
    
    Параметры:
    - user_id (int): Идентификатор пользователя.
    - status (str): Фильтр по статусу бронирования (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Список бронирований пользователя.
    """
    bookings = crud.get_user_bookings(db, user_id=user_id, status=status)
    return bookings

@booking_router.get("/venues/{venue_id}")
def read_venue_bookings(venue_id: int, status: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, db: Session = Depends(get_db)):
    """
    Получает бронирования спортивной площадки с фильтрацией по статусу и дате.
    
    Параметры:
    - venue_id (int): Идентификатор спортивной площадки.
    - status (str): Фильтр по статусу бронирования (опционально).
    - start_date (datetime): Фильтр по начальной дате бронирования (опционально).
    - end_date (datetime): Фильтр по конечной дате бронирования (опционально).
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Список бронирований спортивной площадки.
    """
    bookings = crud.get_venue_bookings(db, venue_id=venue_id, status=status, start_date=start_date, end_date=end_date)
    return bookings

@booking_router.put("/{booking_id}")
def update_booking_status(booking_id: int, status: str, db: Session = Depends(get_db)):
    """
    Обновляет статус бронирования.
    
    Параметры:
    - booking_id (int): Идентификатор бронирования.
    - status (str): Новый статус бронирования.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Обновленное бронирование.
    - Если бронирование не найдено, возвращает None.
    """
    updated_booking = crud.update_booking_status(db, booking_id=booking_id, status=status)
    return updated_booking

@booking_router.post("/{booking_id}/services")
def add_service_to_booking(booking_id: int, service_id: int, db: Session = Depends(get_db)):
    """
    Добавляет услугу к бронированию.
    
    Параметры:
    - booking_id (int): Идентификатор бронирования.
    - service_id (int): Идентификатор услуги.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Объект добавленной услуги бронирования.
    - Если бронирование или услуга не найдены, возвращает None.
    """
    booking_service = crud.add_service_to_booking(db, booking_id=booking_id, service_id=service_id)
    return booking_service

@booking_router.delete("/{booking_id}/services/{service_id}")
def remove_service_from_booking(booking_id: int, service_id: int, db: Session = Depends(get_db)):
    """
    Удаляет услугу из бронирования.
    
    Параметры:
    - booking_id (int): Идентификатор бронирования.
    - service_id (int): Идентификатор услуги.
    - db (Session): Сессия базы данных.
    
    Возвращает:
    - Словарь с ключом "success" и значением True, если услуга успешно удалена, иначе False.
    """
    success = crud.remove_service_from_booking(db, booking_id=booking_id, service_id=service_id)
    return {"success": success}