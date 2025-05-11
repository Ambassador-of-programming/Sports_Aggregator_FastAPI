from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime
from . import models
from typing import List, Optional, Dict, Any


# ================ Функции для управления пользователями ================

def create_user(db: Session, username: str, password: str, avatar_url: Optional[str] = None):
    """
    Создает нового пользователя
    """
    db_user = models.User(username=username, password=password, avatar_url=avatar_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """
    Получает пользователя по ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str, password: str):
    """
    Получает пользователя по имени пользователя
    """
    return db.query(models.User).filter(models.User.username == username, models.User.password == password).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список пользователей с пагинацией
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, data: Dict[str, Any]):
    """
    Обновляет данные пользователя
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    Удаляет пользователя
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def increment_user_followers(db: Session, user_id: int):
    """
    Увеличивает счетчик подписчиков пользователя
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.followers_count += 1
        db.commit()
        return True
    return False

def decrement_user_followers(db: Session, user_id: int):
    """
    Уменьшает счетчик подписчиков пользователя
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user and db_user.followers_count > 0:
        db_user.followers_count -= 1
        db.commit()
        return True
    return False

def increment_user_reviews(db: Session, user_id: int):
    """
    Увеличивает счетчик отзывов пользователя
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.reviews_count += 1
        db.commit()
        return True
    return False


# ================ Функции для управления спортивными категориями ================

def create_sport_category(db: Session, name: str, icon_url: Optional[str] = None):
    """
    Создает новую спортивную категорию
    """
    db_category = models.SportCategory(name=name, icon_url=icon_url)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_sport_category(db: Session, category_id: int):
    """
    Получает спортивную категорию по ID
    """
    return db.query(models.SportCategory).filter(models.SportCategory.id == category_id).first()

def get_sport_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список спортивных категорий с пагинацией
    """
    return db.query(models.SportCategory).offset(skip).limit(limit).all()

def update_sport_category(db: Session, category_id: int, data: Dict[str, Any]):
    """
    Обновляет данные спортивной категории
    """
    db_category = db.query(models.SportCategory).filter(models.SportCategory.id == category_id).first()
    if db_category:
        for key, value in data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_sport_category(db: Session, category_id: int):
    """
    Удаляет спортивную категорию
    """
    db_category = db.query(models.SportCategory).filter(models.SportCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# ================ Функции для управления элементами ленты ================

def create_feed_item(db: Session, title: str, category_id: int, image_url: Optional[str] = None, 
                    is_interesting: bool = False):
    """
    Создает элемент ленты
    """

    db_feed_item = models.FeedItem(
        title=title, 
        category_id=category_id, 
        image_url=image_url, 
        is_interesting=is_interesting
    )
    db.add(db_feed_item)
    db.commit()
    db.refresh(db_feed_item)
    return db_feed_item

def get_feed_item(db: Session, feed_item_id: int):
    """
    Получает элемент ленты по ID
    """
    return db.query(models.FeedItem).filter(models.FeedItem.id == feed_item_id).first()

def get_feed_items(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, 
                   is_interesting: Optional[bool] = None):
    """
    Получает список элементов ленты с пагинацией и фильтрацией
    """
    query = db.query(models.FeedItem)
    
    if category_id:
        query = query.filter(models.FeedItem.category_id == category_id)
    
    if is_interesting is not None:
        query = query.filter(models.FeedItem.is_interesting == is_interesting)
    
    return query.offset(skip).limit(limit).all()

def update_feed_item(db: Session, feed_item_id: int, data: Dict[str, Any]):
    """
    Обновляет данные элемента ленты
    """
    db_feed_item = db.query(models.FeedItem).filter(models.FeedItem.id == feed_item_id).first()
    if db_feed_item:
        for key, value in data.items():
            setattr(db_feed_item, key, value)
        db.commit()
        db.refresh(db_feed_item)
    return db_feed_item

def delete_feed_item(db: Session, feed_item_id: int):
    """
    Удаляет элемент ленты
    """
    db_feed_item = db.query(models.FeedItem).filter(models.FeedItem.id == feed_item_id).first()
    if db_feed_item:
        db.delete(db_feed_item)
        db.commit()
        return True
    return False

def like_feed_item(db: Session, feed_item_id: int, user_id: int):
    """
    Добавляет лайк к элементу ленты от пользователя
    """
    existing_like = db.query(models.FeedLike).filter(
        models.FeedLike.feed_item_id == feed_item_id,
        models.FeedLike.user_id == user_id
    ).first()
    
    if existing_like:
        return existing_like
    
    # Создаем новый лайк
    db_like = models.FeedLike(feed_item_id=feed_item_id, user_id=user_id)
    db.add(db_like)
    
    # Увеличиваем счетчик лайков
    db_feed_item = db.query(models.FeedItem).filter(models.FeedItem.id == feed_item_id).first()
    if db_feed_item:
        db_feed_item.likes_count += 1
    
    db.commit()
    db.refresh(db_like)
    return db_like

def unlike_feed_item(db: Session, feed_item_id: int, user_id: int):
    """
    Удаляет лайк пользователя от элемента ленты
    """
    db_like = db.query(models.FeedLike).filter(
        models.FeedLike.feed_item_id == feed_item_id,
        models.FeedLike.user_id == user_id
    ).first()
    
    if db_like:
        db.delete(db_like)
        
        # Уменьшаем счетчик лайков
        db_feed_item = db.query(models.FeedItem).filter(models.FeedItem.id == feed_item_id).first()
        if db_feed_item and db_feed_item.likes_count > 0:
            db_feed_item.likes_count -= 1
        
        db.commit()
        return True
    
    return False

def increment_feed_item_views(db: Session, feed_item_id: int):
    """
    Увеличивает счетчик просмотров элемента ленты
    """
    db_feed_item = db.query(models.FeedItem).filter(models.FeedItem.id == feed_item_id).first()
    if db_feed_item:
        db_feed_item.views_count += 1
        db.commit()
        return True
    return False

# ================ Функции для управления мероприятиями ================

def create_event(db: Session, data: Dict[str, Any]):
    """
    Создает новое мероприятие
    """
    db_event = models.Event(**data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    """
    Получает мероприятие по ID
    """
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, 
               status: Optional[str] = None, owner_id: Optional[int] = None,
               min_date: Optional[datetime] = None, max_date: Optional[datetime] = None,
               latitude: Optional[float] = None, longitude: Optional[float] = None,
               distance: Optional[float] = None):
    
    """
    Получает список мероприятий с пагинацией и фильтрацией
    """
    
    query = db.query(models.Event)
    
    if category_id:
        query = query.filter(models.Event.sport_category_id == category_id)
    
    if status:
        query = query.filter(models.Event.status == status)
    
    if owner_id:
        query = query.filter(models.Event.owner_id == owner_id)
    
    if min_date:
        query = query.filter(models.Event.event_date >= min_date)
    
    if max_date:
        query = query.filter(models.Event.event_date <= max_date)
    
    # Фильтрация по геолокации если предоставлены координаты и расстояние
    if latitude and longitude and distance:
        # Примечание: для точного расчета расстояния по GPS координатам 
        # требуется использовать PostgreSQL функцию ST_Distance или написать
        # собственную функцию, использующую формулу гаверсинусов
        # Упрощенный вариант для демонстрации:
        earth_radius = 6371  # км
        # Приблизительный расчет расстояния в прямоугольной области
        lat_km = distance / earth_radius * (180 / 3.14)
        lon_km = distance / (earth_radius * func.cos(latitude * 3.14 / 180)) * (180 / 3.14)
        
        query = query.filter(
            and_(
                models.Event.latitude.between(latitude - lat_km, latitude + lat_km),
                models.Event.longitude.between(longitude - lon_km, longitude + lon_km)
            )
        )
    
    return query.offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, data: Dict[str, Any]):
    """
    Обновляет данные мероприятия
    """
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        for key, value in data.items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    """
    Удаляет мероприятие
    """

    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False

def like_event(db: Session, event_id: int, user_id: int):
    """
    Добавляет лайк к мероприятию от пользователя
    """
    existing_like = db.query(models.EventLike).filter(
        models.EventLike.event_id == event_id,
        models.EventLike.user_id == user_id
    ).first()
    
    if existing_like:
        return existing_like
    
    db_like = models.EventLike(event_id=event_id, user_id=user_id)
    db.add(db_like)
    
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db_event.likes_count += 1
    
    db.commit()
    db.refresh(db_like)
    return db_like

def unlike_event(db: Session, event_id: int, user_id: int):
    """
    Удаляет лайк пользователя от мероприятия
    """
    db_like = db.query(models.EventLike).filter(
        models.EventLike.event_id == event_id,
        models.EventLike.user_id == user_id
    ).first()
    
    if db_like:
        db.delete(db_like)
        
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if db_event and db_event.likes_count > 0:
            db_event.likes_count -= 1
        
        db.commit()
        return True
    
    return False

def increment_event_views(db: Session, event_id: int):
    """
    Увеличивает счетчик просмотров мероприятия
    """
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db_event.views_count += 1
        db.commit()
        return True
    return False

def register_for_event(db: Session, event_id: int, user_id: int):
    """
    Регистрирует пользователя на мероприятие
    """
    # Проверка существующей регистрации
    existing_reg = db.query(models.EventRegistration).filter(
        models.EventRegistration.event_id == event_id,
        models.EventRegistration.user_id == user_id
    ).first()
    
    if existing_reg:
        return existing_reg
    
    # Проверка доступности мест
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event or event.available_seats <= 0:
        return None
    
    # Создание регистрации
    db_registration = models.EventRegistration(
        event_id=event_id, 
        user_id=user_id
    )
    db.add(db_registration)
    
    # Уменьшение количества доступных мест
    event.available_seats -= 1
    
    db.commit()
    db.refresh(db_registration)
    return db_registration

def check_event_user(db: Session, user_id: int):
    """
    Проверяет, зарегистрирован ли пользователь на мероприятие
    """
    return db.query(models.EventRegistration).filter(models.EventRegistration.user_id == user_id).all()

# ================ Функции для управления площадками ================

def create_venue(db: Session, data: Dict[str, Any]):
    """
    Создает новую спортивную площадку
    """

    db_venue = models.Venue(**data)
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

def get_venue(db: Session, venue_id: int):
    """
    Получает спортивную площадку по ID
    """
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()

def get_venues(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, 
               venue_type: Optional[str] = None, owner_id: Optional[int] = None):
    """
    Получает список спортивных площадок с пагинацией и фильтрацией
    """
    query = db.query(models.Venue)
    
    if category_id:
        query = query.filter(models.Venue.sport_category_id == category_id)
    
    if venue_type:
        query = query.filter(models.Venue.venue_type == venue_type)
    
    if owner_id:
        query = query.filter(models.Venue.owner_id == owner_id)
    
    return query.offset(skip).limit(limit).all()

def update_venue(db: Session, venue_id: int, data: Dict[str, Any]):
    """
    Обновляет данные спортивной площадки
    """
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if db_venue:
        for key, value in data.items():
            setattr(db_venue, key, value)
        db.commit()
        db.refresh(db_venue)
    return db_venue

def delete_venue(db: Session, venue_id: int):
    """
    Удаляет спортивную площадку
    """
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if db_venue:
        db.delete(db_venue)
        db.commit()
        return True
    return False

def like_venue(db: Session, venue_id: int, user_id: int):
    """
    Добавляет лайк к спортивной площадке от пользователя
    """
    existing_like = db.query(models.VenueLike).filter(
        models.VenueLike.venue_id == venue_id,
        models.VenueLike.user_id == user_id
    ).first()
    
    if existing_like:
        return existing_like
    
    db_like = models.VenueLike(venue_id=venue_id, user_id=user_id)
    db.add(db_like)
    
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if db_venue:
        db_venue.likes_count += 1
    
    db.commit()
    db.refresh(db_like)
    return db_like

def unlike_venue(db: Session, venue_id: int, user_id: int):
    """
    Удаляет лайк пользователя от спортивной площадки
    """
    db_like = db.query(models.VenueLike).filter(
        models.VenueLike.venue_id == venue_id,
        models.VenueLike.user_id == user_id
    ).first()
    
    if db_like:
        db.delete(db_like)
        
        db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
        if db_venue and db_venue.likes_count > 0:
            db_venue.likes_count -= 1
        
        db.commit()
        return True

# ================ Функции для управления командами ================

def create_team(db: Session, name: str, sport_category_id: int, creator_id: int, 
                capacity: int = 10, logo_url: Optional[str] = None, 
                is_auto_team: bool = False, event_id: Optional[int] = None):
    """
    Создает новую команду
    """
    db_team = models.Team(
        name=name,
        sport_category_id=sport_category_id,
        creator_id=creator_id,
        capacity=capacity,
        current_members=1,  # Создатель автоматически становится членом команды
        logo_url=logo_url,
        is_auto_team=is_auto_team,
        event_id=event_id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    # Добавляем создателя как капитана команды
    db_member = models.TeamMember(
        team_id=db_team.id,
        user_id=creator_id,
        role='captain'
    )
    db.add(db_member)
    
    # Создаем статистику команды
    db_stats = models.TeamStats(
        team_id=db_team.id
    )
    db.add(db_stats)
    
    db.commit()
    return db_team

def get_team(db: Session, team_id: int):
    """
    Получает команду по ID
    """
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_member(db: Session, team_id: int, user_id: int):
    """
    Получает команду по ID
    """
    
    zapros = db.query(models.Team).filter(models.TeamMember.team_id == team_id, models.TeamMember.user_id == user_id).first()
    if zapros:
        return zapros
    
    return None
def get_teams(db: Session, skip: int = 0, limit: int = 100, 
              sport_category_id: Optional[int] = None, 
              event_id: Optional[int] = None,
              is_auto_team: Optional[bool] = None):
    """
    Получает список команд с фильтрацией
    """
    query = db.query(models.Team)
    
    if sport_category_id:
        query = query.filter(models.Team.sport_category_id == sport_category_id)
    
    if event_id:
        query = query.filter(models.Team.event_id == event_id)
    
    if is_auto_team is not None:
        query = query.filter(models.Team.is_auto_team == is_auto_team)
    
    return query.offset(skip).limit(limit).all()

def update_team(db: Session, team_id: int, data: Dict[str, Any]):
    """
    Обновляет данные команды
    """
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        for key, value in data.items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int):
    """
    Удаляет команду
    """
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
        return True
    return False

def add_team_member(db: Session, team_id: int, user_id: int, 
                    role: str = 'player', position: Optional[str] = None):
    """
    Добавляет пользователя в команду
    """
    # Проверяем, существует ли уже членство
    existing_member = db.query(models.TeamMember).filter(
        models.TeamMember.team_id == team_id,
        models.TeamMember.user_id == user_id
    ).first()
    
    if existing_member:
        return existing_member
    
    # Проверяем, есть ли место в команде
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team or team.current_members >= team.capacity:
        return None
    
    # Добавляем пользователя в команду
    db_member = models.TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=role,
        position=position
    )
    db.add(db_member)
    
    # Увеличиваем счетчик членов команды
    team.current_members += 1
    
    db.commit()
    db.refresh(db_member)
    return db_member

def remove_team_member(db: Session, team_id: int, user_id: int):
    """
    Удаляет пользователя из команды
    """
    db_member = db.query(models.TeamMember).filter(
        models.TeamMember.team_id == team_id,
        models.TeamMember.user_id == user_id
    ).first()
    
    if db_member:
        # Проверяем, не является ли пользователь капитаном
        if db_member.role == 'captain':
            # Проверяем, есть ли другие члены команды
            other_members = db.query(models.TeamMember).filter(
                models.TeamMember.team_id == team_id,
                models.TeamMember.user_id != user_id
            ).first()
            
            # Если капитан - единственный в команде, разрешаем удаление
            if not other_members:
                db.delete(db_member)
                
                # Уменьшаем счетчик членов команды
                team = db.query(models.Team).filter(models.Team.id == team_id).first()
                if team and team.current_members > 0:
                    team.current_members -= 1
                
                db.commit()
                return True
            else:
                # Капитан не может покинуть команду, если есть другие члены
                return False
        else:
            # Обычный игрок может быть удален
            db.delete(db_member)
            
            # Уменьшаем счетчик членов команды
            team = db.query(models.Team).filter(models.Team.id == team_id).first()
            if team and team.current_members > 0:
                team.current_members -= 1
            
            db.commit()
            return True
    
    return False

def update_team_member(db: Session, team_id: int, user_id: int, data: Dict[str, Any]):
    """
    Обновляет данные члена команды
    """
    db_member = db.query(models.TeamMember).filter(
        models.TeamMember.team_id == team_id,
        models.TeamMember.user_id == user_id
    ).first()
    
    if db_member:
        for key, value in data.items():
            setattr(db_member, key, value)
        db.commit()
        db.refresh(db_member)
    
    return db_member

def create_team_request(db: Session, team_id: int, user_id: int):
    """
    Создает запрос на вступление в команду
    """
    # Проверяем, существует ли уже запрос
    existing_request = db.query(models.TeamRequest).filter(
        models.TeamRequest.team_id == team_id,
        models.TeamRequest.user_id == user_id
    ).first()
    
    if existing_request:
        return existing_request
    
    # Проверяем, не является ли пользователь уже членом команды
    existing_member = db.query(models.TeamMember).filter(
        models.TeamMember.team_id == team_id,
        models.TeamMember.user_id == user_id
    ).first()
    
    if existing_member:
        return None
    
    db_request = models.TeamRequest(
        team_id=team_id,
        user_id=user_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def handle_team_request(db: Session, request_id: int, status: str):
    """
    Обрабатывает запрос на вступление в команду (принятие или отклонение)
    """
    db_request = db.query(models.TeamRequest).filter(models.TeamRequest.id == request_id).first()
    
    if not db_request:
        return None
    
    db_request.status = status
    db.commit()
    
    # Если запрос принят, добавляем пользователя в команду
    if status == 'accepted':
        add_team_member(db, db_request.team_id, db_request.user_id)
    
    db.refresh(db_request)
    return db_request

def update_team_stats(db: Session, team_id: int, data: Dict[str, Any]):
    """
    Обновляет статистику команды
    """
    db_stats = db.query(models.TeamStats).filter(models.TeamStats.team_id == team_id).first()
    
    if not db_stats:
        # Создаем статистику, если не существует
        db_stats = models.TeamStats(team_id=team_id)
        db.add(db_stats)
    
    for key, value in data.items():
        setattr(db_stats, key, value)
    
    # Обновляем процент побед
    if 'matches_played' in data and data['matches_played'] > 0 and 'wins' in data:
        db_stats.win_percentage = (db_stats.wins / db_stats.matches_played) * 100
    
    db.commit()
    db.refresh(db_stats)
    return db_stats

# ================ Функции для управления временными слотами ================

def create_time_slot(db: Session, venue_id: int, start_time: datetime, end_time: datetime, 
                     date: Optional[datetime] = None, is_available: bool = True):
    """
    Создает временной слот для площадки
    """
    db_time_slot = models.TimeSlot(
        venue_id=venue_id,
        date=date or start_time.date(),
        start_time=start_time,
        end_time=end_time,
        is_available=is_available
    )
    db.add(db_time_slot)
    db.commit()
    db.refresh(db_time_slot)
    return db_time_slot

def get_time_slot(db: Session, time_slot_id: int):
    """
    Получает временной слот по ID
    """
    return db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()

def get_venue_time_slots(db: Session, venue_id: int, start_date: Optional[datetime] = None, 
                         end_date: Optional[datetime] = None, is_available: Optional[bool] = None):
    """
    Получает временные слоты для площадки с фильтрацией
    """
    query = db.query(models.TimeSlot).filter(models.TimeSlot.venue_id == venue_id)
    
    if start_date:
        query = query.filter(models.TimeSlot.date >= start_date.date())
    
    if end_date:
        query = query.filter(models.TimeSlot.date <= end_date.date())
    
    if is_available is not None:
        query = query.filter(models.TimeSlot.is_available == is_available)
    
    return query.order_by(models.TimeSlot.date, models.TimeSlot.start_time).all()

def update_time_slot(db: Session, time_slot_id: int, data: Dict[str, Any]):
    """
    Обновляет данные временного слота
    """
    db_time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    if db_time_slot:
        for key, value in data.items():
            setattr(db_time_slot, key, value)
        db.commit()
        db.refresh(db_time_slot)
    return db_time_slot

def delete_time_slot(db: Session, time_slot_id: int):
    """
    Удаляет временной слот
    """
    db_time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    if db_time_slot:
        db.delete(db_time_slot)
        db.commit()
        return True
    return False

# ================ Функции для управления услугами площадки ================

def create_venue_service(db: Session, venue_id: int, name: str, price: float, 
                         description: Optional[str] = None, is_active: bool = True):
    """
    Создает услугу для площадки
    """
    db_service = models.VenueService(
        venue_id=venue_id,
        name=name,
        description=description,
        price=price,
        is_active=is_active
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_venue_service(db: Session, service_id: int):
    """
    Получает услугу по ID
    """
    return db.query(models.VenueService).filter(models.VenueService.id == service_id).first()

def get_venue_services(db: Session, venue_id: int, is_active: Optional[bool] = None):
    """
    Получает услуги для площадки с фильтрацией
    """
    query = db.query(models.VenueService).filter(models.VenueService.venue_id == venue_id)
    
    if is_active is not None:
        query = query.filter(models.VenueService.is_active == is_active)
    
    return query.order_by(models.VenueService.name).all()

def update_venue_service(db: Session, service_id: int, data: Dict[str, Any]):
    """
    Обновляет данные услуги
    """
    db_service = db.query(models.VenueService).filter(models.VenueService.id == service_id).first()
    if db_service:
        for key, value in data.items():
            setattr(db_service, key, value)
        db.commit()
        db.refresh(db_service)
    return db_service

def delete_venue_service(db: Session, service_id: int):
    """
    Удаляет услугу
    """
    db_service = db.query(models.VenueService).filter(models.VenueService.id == service_id).first()
    if db_service:
        db.delete(db_service)
        db.commit()
        return True
    return False

# ================ Функции для управления бронированиями ================

def create_booking(db: Session, user_id: int, venue_id: int, time_slot_id: int):
    """
    Создает бронирование площадки
    """
    # Проверяем доступность временного слота
    # time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    # if not time_slot or not time_slot.is_available:
    #     return None
    
    # Создаем бронирование
    db_booking = models.Booking(
        user_id=user_id,
        venue_id=venue_id,
        time_slot_id=time_slot_id,
        status='created',
        total_price=0  # Изначально цена нулевая, будет обновлена при добавлении услуг
    )
    db.add(db_booking)
    
    # Помечаем временной слот как недоступный
    # time_slot.is_available = False
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking(db: Session, booking_id: int):
    """
    Получает бронирование по ID
    """
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_user_bookings(db: Session, user_id: int, status: Optional[str] = None):
    """
    Получает бронирования пользователя с фильтрацией
    """
    query = db.query(models.Booking).filter(models.Booking.user_id == user_id)
    
    if status:
        query = query.filter(models.Booking.status == status)
    
    return query.order_by(models.Booking.booking_date.desc()).all()

def get_venue_bookings(db: Session, venue_id: int, status: Optional[str] = None, 
                       start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    """
    Получает бронирования площадки с фильтрацией
    """
    query = db.query(models.Booking).filter(models.Booking.venue_id == venue_id)
    
    if status:
        query = query.filter(models.Booking.status == status)
    
    if start_date or end_date:
        # Присоединяем временные слоты для фильтрации по дате
        query = query.join(models.TimeSlot, models.Booking.time_slot_id == models.TimeSlot.id)
        
        if start_date:
            query = query.filter(models.TimeSlot.date >= start_date.date())
        
        if end_date:
            query = query.filter(models.TimeSlot.date <= end_date.date())
    
    return query.order_by(models.Booking.booking_date.desc()).all()

def update_booking_status(db: Session, booking_id: int, status: str):
    """
    Обновляет статус бронирования
    """
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db_booking.status = status
        
        # Если бронирование отменено, освобождаем временной слот
        if status == 'cancelled':
            time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == db_booking.time_slot_id).first()
            if time_slot:
                time_slot.is_available = True
        
        db.commit()
        db.refresh(db_booking)
    return db_booking

def add_service_to_booking(db: Session, booking_id: int, service_id: int):
    """
    Добавляет услугу к бронированию
    """
    # Проверяем существование бронирования и услуги
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    service = db.query(models.VenueService).filter(
        models.VenueService.id == service_id,
        models.VenueService.venue_id == booking.venue_id,
        models.VenueService.is_active == True
    ).first()
    
    if not booking or not service:
        return None
    
    # Проверяем, не добавлена ли уже услуга к бронированию
    existing_service = db.query(models.BookingService).filter(
        models.BookingService.booking_id == booking_id,
        models.BookingService.service_id == service_id
    ).first()
    
    if existing_service:
        return existing_service
    
    # Добавляем услугу
    db_booking_service = models.BookingService(
        booking_id=booking_id,
        service_id=service_id
    )
    db.add(db_booking_service)
    
    # Обновляем общую стоимость бронирования
    booking.total_price += service.price
    
    db.commit()
    db.refresh(db_booking_service)
    return db_booking_service

def remove_service_from_booking(db: Session, booking_id: int, service_id: int):
    """
    Удаляет услугу из бронирования
    """
    db_booking_service = db.query(models.BookingService).filter(
        models.BookingService.booking_id == booking_id,
        models.BookingService.service_id == service_id
    ).first()
    
    if db_booking_service:
        # Уменьшаем общую стоимость бронирования
        service = db.query(models.VenueService).filter(models.VenueService.id == service_id).first()
        booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
        
        if service and booking and booking.total_price >= service.price:
            booking.total_price -= service.price
        
        db.delete(db_booking_service)
        db.commit()
        return True
    
    return False

# ================ Функции для управления командными регистрациями на мероприятия ================

def register_team_for_event(db: Session, event_id: int, team_id: int, 
                           individual_fee: float = 0, team_fee: float = 0):
    """
    Регистрирует команду на мероприятие
    """
    # Проверяем существующую регистрацию
    existing_reg = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.event_id == event_id,
        models.EventTeamRegistration.team_id == team_id
    ).first()
    
    if existing_reg:
        return existing_reg
    
    # Проверяем наличие мероприятия и команды
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    
    if not event or not team:
        return None
    
    # Создаем регистрацию
    db_registration = models.EventTeamRegistration(
        event_id=event_id,
        team_id=team_id,
        individual_fee=individual_fee,
        team_fee=team_fee
    )
    db.add(db_registration)
    
    # Если у мероприятия есть ограничение по количеству участников и команд,
    # нужно соответственно уменьшить количество доступных мест
    if event.available_seats > 0:
        event.available_seats -= 1
    
    db.commit()
    db.refresh(db_registration)
    return db_registration

def get_team_event_registration(db: Session, registration_id: int):
    """
    Получает регистрацию команды на мероприятие по ID
    """
    return db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.id == registration_id
    ).first()

def get_event_team_registrations(db: Session, event_id: int, status: Optional[str] = None):
    """
    Получает все регистрации команд на мероприятие с фильтрацией
    """
    query = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.event_id == event_id
    )
    
    if status:
        query = query.filter(models.EventTeamRegistration.status == status)
    
    return query.all()

def get_team_event_registrations(db: Session, team_id: int, status: Optional[str] = None):
    """
    Получает все регистрации команды на мероприятия с фильтрацией
    """
    query = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.team_id == team_id
    )
    
    if status:
        query = query.filter(models.EventTeamRegistration.status == status)
    
    return query.all()

def update_team_registration_status(db: Session, registration_id: int, status: str):
    """
    Обновляет статус регистрации команды на мероприятие
    """
    db_registration = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.id == registration_id
    ).first()
    
    if db_registration:
        old_status = db_registration.status
        db_registration.status = status
        
        # Если регистрация была отклонена, нужно вернуть место в мероприятии
        if old_status != 'rejected' and status == 'rejected':
            event = db.query(models.Event).filter(models.Event.id == db_registration.event_id).first()
            if event:
                event.available_seats += 1
        
        # Если ранее отклоненная регистрация была одобрена, нужно снова занять место
        elif old_status == 'rejected' and status == 'approved':
            event = db.query(models.Event).filter(models.Event.id == db_registration.event_id).first()
            if event and event.available_seats > 0:
                event.available_seats -= 1
        
        db.commit()
        db.refresh(db_registration)
    
    return db_registration

def update_team_registration_payment(db: Session, registration_id: int, payment_status: str):
    """
    Обновляет статус оплаты регистрации команды на мероприятие
    """
    db_registration = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.id == registration_id
    ).first()
    
    if db_registration:
        db_registration.payment_status = payment_status
        db.commit()
        db.refresh(db_registration)
    
    return db_registration

def update_team_registration_fees(db: Session, registration_id: int, individual_fee: Optional[float] = None, 
                                 team_fee: Optional[float] = None):
    """
    Обновляет суммы взносов для регистрации команды на мероприятие
    """
    db_registration = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.id == registration_id
    ).first()
    
    if db_registration:
        if individual_fee is not None:
            db_registration.individual_fee = individual_fee
        
        if team_fee is not None:
            db_registration.team_fee = team_fee
        
        db.commit()
        db.refresh(db_registration)
    
    return db_registration

def delete_team_registration(db: Session, registration_id: int):
    """
    Удаляет регистрацию команды на мероприятие
    """
    db_registration = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.id == registration_id
    ).first()
    
    if db_registration:
        # Возвращаем место в мероприятии, если статус не был "отклонен"
        if db_registration.status != 'rejected':
            event = db.query(models.Event).filter(models.Event.id == db_registration.event_id).first()
            if event:
                event.available_seats += 1
        
        db.delete(db_registration)
        db.commit()
        return True
    
    return False

def calculate_team_registration_total(db: Session, registration_id: int):
    """
    Рассчитывает общую сумму оплаты для команды (командный взнос + индивидуальные взносы)
    """
    db_registration = db.query(models.EventTeamRegistration).filter(
        models.EventTeamRegistration.id == registration_id
    ).first()
    
    if not db_registration:
        return None
    
    # Получаем команду и количество участников
    team = db.query(models.Team).filter(models.Team.id == db_registration.team_id).first()
    
    if not team:
        return None
    
    # Расчет общей суммы: командный взнос + (индивидуальный взнос * количество участников)
    total = db_registration.team_fee + (db_registration.individual_fee * team.current_members)
    
    return {"total": total, "team_fee": db_registration.team_fee, 
            "individual_fee": db_registration.individual_fee, 
            "members_count": team.current_members}