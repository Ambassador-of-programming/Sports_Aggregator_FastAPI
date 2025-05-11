from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import crud
from database.base import get_db


# Маршруты для команд
team_router = APIRouter()


@team_router.post("/")
def create_team(name: str, sport_category_id: int, creator_id: int, capacity: int = 10, logo_url: Optional[str] = None, is_auto_team: bool = False, event_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Создает новую команду.

    Параметры:
    - name (str): Название команды (обязательный).
    - sport_category_id (int): Идентификатор спортивной категории (обязательный).
    - creator_id (int): Идентификатор пользователя-создателя команды (обязательный).
    - capacity (int): Вместимость команды (по умолчанию: 10).
    - logo_url (str): URL логотипа команды (опционально).
    - is_auto_team (bool): Флаг, указывающий, является ли команда автоматически сформированной (по умолчанию: False).
    - event_id (int): Идентификатор мероприятия, к которому привязана команда (опционально).
    - db (Session): Сессия базы данных.

    Возвращает:
    - Созданную команду.
    """
    cread_team = crud.create_team(db=db, name=name, sport_category_id=sport_category_id, creator_id=creator_id,
                                  capacity=capacity, logo_url=logo_url, is_auto_team=is_auto_team, event_id=event_id)
    team_dict = {
        column.name: getattr(cread_team, column.name)
        for column in cread_team.__table__.columns
    }


    return team_dict


@team_router.get("/{team_id}")
def read_team(team_id: int, db: Session = Depends(get_db)):
    """
    Получает команду по ее идентификатору.

    Параметры:
    - team_id (int): Идентификатор команды.
    - db (Session): Сессия базы данных.

    Возвращает:
    - Команду.

    Исключения:
    - HTTPException (status_code=404): Если команда не найдена.
    """
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return db_team


@team_router.get("/")
def read_teams(skip: int = 0, limit: int = 100, sport_category_id: Optional[int] = None, event_id: Optional[int] = None, is_auto_team: Optional[bool] = None, db: Session = Depends(get_db)):
    """
    Получает список команд с пагинацией и фильтрацией.

    Параметры:
    - skip (int): Количество команд, которые нужно пропустить (по умолчанию: 0).
    - limit (int): Максимальное количество команд, которые нужно вернуть (по умолчанию: 100).
    - sport_category_id (int): Фильтр по идентификатору спортивной категории (опционально).
    - event_id (int): Фильтр по идентификатору мероприятия (опционально).
    - is_auto_team (bool): Фильтр по флагу автоматически сформированной команды (опционально).
    - db (Session): Сессия базы данных.

    Возвращает:
    - Список команд.
    """
    teams = crud.get_teams(db, skip=skip, limit=limit, sport_category_id=sport_category_id,
                           event_id=event_id, is_auto_team=is_auto_team)
    return teams


@team_router.put("/{team_id}")
def update_team(team_id: int, name: Optional[str] = None, sport_category_id: Optional[int] = None, capacity: Optional[int] = None, logo_url: Optional[str] = None, is_auto_team: Optional[bool] = None, event_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные команды.

    Параметры:
    - team_id (int): Идентификатор команды.
    - name (str): Новое название команды (опционально).
    - sport_category_id (int): Новый идентификатор спортивной категории (опционально).
    - capacity (int): Новая вместимость команды (опционально).
    - logo_url (str): Новый URL логотипа команды (опционально).
    - is_auto_team (bool): Новый флаг автоматически сформированной команды (опционально).
    - event_id (int): Новый идентификатор мероприятия, к которому привязана команда (опционально).
    - db (Session): Сессия базы данных.

    Возвращает:
    - Обновленную команду.

    Исключения:
    - HTTPException (status_code=404): Если команда не найдена.
    """
    team_data = {}
    if name is not None:
        team_data["name"] = name
    if sport_category_id is not None:
        team_data["sport_category_id"] = sport_category_id
    if capacity is not None:
        team_data["capacity"] = capacity
    if logo_url is not None:
        team_data["logo_url"] = logo_url
    if is_auto_team is not None:
        team_data["is_auto_team"] = is_auto_team
    if event_id is not None:
        team_data["event_id"] = event_id

    updated_team = crud.update_team(db, team_id=team_id, data=team_data)
    if updated_team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return updated_team


@team_router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """
    Удаляет команду.

    Параметры:
    - team_id (int): Идентификатор команды.
    - db (Session): Сессия базы данных.

    Возвращает:
    - Словарь с ключом "success" и значением True, если команда успешно удалена, иначе False.
    """
    success = crud.delete_team(db, team_id=team_id)
    return {"success": success}


@team_router.post("/{team_id}/members")
def add_team_member(team_id: int, user_id: int, role: str = 'player', position: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Добавляет пользователя в команду.

    Параметры:
    - team_id (int): Идентификатор команды.
    - user_id (int): Идентификатор пользователя.
    - role (str): Роль пользователя в команде (по умолчанию: 'player').
    - position (str): Позиция игрока в команде (опционально).
    - db (Session): Сессия базы данных.

    Возвращает:
    - Объект члена команды.
    - Если команда заполнена или пользователь уже является членом команды, возвращает None.
    """
    team_member = crud.add_team_member(
        db, team_id=team_id, user_id=user_id, role=role, position=position)
    return team_member


@team_router.get("/{team_id}/members")
def get_team_member(team_id: int, user_id: int,  db: Session = Depends(get_db)):
    """
    Добавляет пользователя в команду.

    Параметры:
    - team_id (int): Идентификатор команды.
    - user_id (int): Идентификатор пользователя.
    - db (Session): Сессия базы данных.

    Возвращает:
    - Объект члена команды.
    - Если команда заполнена или пользователь уже является членом команды, возвращает None.
    """
    team_member = crud.get_team_member(db, team_id=team_id, user_id=user_id)
    if team_member is None:
        raise HTTPException(
            status_code=404, detail="Пользователь не найден в команде")
    return team_member


@team_router.delete("/{team_id}/members/{user_id}")
def remove_team_member(team_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет пользователя из команды.

    Параметры:
    - team_id (int): Идентификатор команды.
    - user_id (int): Идентификатор пользователя.
    - db (Session): Сессия базы данных.

    Возвращает:
    - Словарь с ключом "success" и значением True, если пользователь успешно удален, иначе False.
    - Если пользователь является капитаном и в команде есть другие члены, возвращает False.
    """
    success = crud.remove_team_member(db, team_id=team_id, user_id=user_id)
    return {"success": success}


@team_router.put("/{team_id}/members/{user_id}")
def update_team_member(team_id: int, user_id: int, role: Optional[str] = None, position: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Обновляет данные члена команды.

    Параметры:
    - team_id (int): Идентификатор команды.
    - user_id (int): Идентификатор пользователя.
    - role (str): Новая роль пользователя в команде (опционально).
    - position (str): Новая позиция игрока в команде (опционально).
    - db (Session): Сессия базы данных.

    Возвращает:
    - Обновленный объект члена команды.
    - Если член команды не найден, возвращает None.
    """
    member_data = {}
    if role is not None:
        member_data["role"] = role
    if position is not None:
        member_data["position"] = position

    updated_member = crud.update_team_member(
        db, team_id=team_id, user_id=user_id, data=member_data)
    return updated_member


@team_router.post("/{team_id}/requests")
def create_team_request(team_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Создает запрос на вступление в команду.

    Параметры:
    - team_id (int): Идентификатор команды.
    - user_id (int): Идентификатор пользователя.
    - db (Session): Сессия базы данных.

    Возвращает:
    - Созданный запрос на вступление в команду.
    - Если запрос уже существует или пользователь уже является членом команды, возвращает None.
    """
    team_request = crud.create_team_request(
        db, team_id=team_id, user_id=user_id)
    return team_request


@team_router.put("/requests/{request_id}")
def handle_team_request(request_id: int, status: str, db: Session = Depends(get_db)):
    """
    Обрабатывает запрос на вступление в команду.

    Параметры:
    - request_id (int): Идентификатор запроса на вступление в команду.
    - status (str): Новый статус запроса ('accepted' или 'rejected').
    - db (Session): Сессия базы данных.

    Возвращает:
    - Обновленный запрос на вступление в команду.
    - Если запрос не найден, возвращает None.
    """
    updated_request = crud.handle_team_request(
        db, request_id=request_id, status=status)
    return updated_request


@team_router.put("/{team_id}/stats")
def update_team_stats(team_id: int, matches_played: Optional[int] = None, wins: Optional[int] = None, goals_scored: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Обновляет статистику команды.

    Параметры:
    - team_id (int): Идентификатор команды.
    - matches_played (int): Количество сыгранных матчей (опционально).
    - wins (int): Количество побед (опционально).
    - goals_scored (int): Количество забитых голов (опционально).
    - db (Session): Сессия базы данных.

    Возвращает:
    - Обновленную статистику команды.
    """
    stats_data = {}
    if matches_played is not None:
        stats_data["matches_played"] = matches_played
    if wins is not None:
        stats_data["wins"] = wins
    if goals_scored is not None:
        stats_data["goals_scored"] = goals_scored

    updated_stats = crud.update_team_stats(
        db, team_id=team_id, data=stats_data)
    return updated_stats
