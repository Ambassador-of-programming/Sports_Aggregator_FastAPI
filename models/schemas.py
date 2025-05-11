from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ============= Базовые модели для ответов =============

class ActionResponse(BaseModel):
    success: bool

class DeleteResponse(BaseModel):
    success: bool


# ============= Модели для пользователей =============

class UserBase(BaseModel):
    username: str
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    followers_count: Optional[int] = None
    reviews_count: Optional[int] = None

class User(UserBase):
    id: int
    followers_count: int = 0
    reviews_count: int = 0

    class Config:
        orm_mode = True


# ============= Модели для спортивных категорий =============

class SportCategoryBase(BaseModel):
    name: str
    icon_url: Optional[str] = None

class SportCategoryCreate(SportCategoryBase):
    pass

class SportCategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon_url: Optional[str] = None

class SportCategory(SportCategoryBase):
    id: int

    class Config:
        orm_mode = True


# ============= Модели для элементов ленты =============

class FeedItemBase(BaseModel):
    title: str
    image_url: Optional[str] = None
    category_id: int
    is_interesting: bool = False

class FeedItemCreate(FeedItemBase):
    pass

class FeedItemUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_interesting: Optional[bool] = None

class FeedItem(FeedItemBase):
    id: int
    views_count: int = 0
    likes_count: int = 0

    class Config:
        orm_mode = True

class FeedLike(BaseModel):
    id: int
    feed_item_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ============= Модели для мероприятий =============

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    sport_category_id: int
    event_date: datetime
    registration_end_date: Optional[datetime] = None
    price: float = 0.0
    available_seats: int = 0
    total_seats: int = 0
    location: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    competition_rules: Optional[str] = None
    owner_id: int
    status: str = "new"  # new, active, completed

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    sport_category_id: Optional[int] = None
    event_date: Optional[datetime] = None
    registration_end_date: Optional[datetime] = None
    price: Optional[float] = None
    available_seats: Optional[int] = None
    total_seats: Optional[int] = None
    location: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    competition_rules: Optional[str] = None
    owner_id: Optional[int] = None
    status: Optional[str] = None

class Event(EventBase):
    id: int
    views_count: int = 0
    likes_count: int = 0

    class Config:
        orm_mode = True

class EventLike(BaseModel):
    id: int
    event_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class EventRegistration(BaseModel):
    id: int
    event_id: int
    user_id: int
    registration_date: datetime
    status: str  # pending, approved, rejected

    class Config:
        orm_mode = True


# ============= Модели для площадок =============

class VenueBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    owner_id: int
    venue_type: Optional[str] = None
    sport_category_id: int

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    owner_id: Optional[int] = None
    venue_type: Optional[str] = None
    sport_category_id: Optional[int] = None

class Venue(VenueBase):
    id: int
    views_count: int = 0
    likes_count: int = 0

    class Config:
        orm_mode = True

class VenueLike(BaseModel):
    id: int
    venue_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TimeSlotBase(BaseModel):
    venue_id: int
    date: Optional[datetime] = None
    start_time: datetime
    end_time: datetime
    is_available: bool = True

class TimeSlotCreate(TimeSlotBase):
    pass

class TimeSlotUpdate(BaseModel):
    date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_available: Optional[bool] = None

class TimeSlot(TimeSlotBase):
    id: int

    class Config:
        orm_mode = True

class VenueServiceBase(BaseModel):
    venue_id: int
    name: str
    description: Optional[str] = None
    price: float = 0.0
    is_active: bool = True

class VenueServiceCreate(VenueServiceBase):
    pass

class VenueServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class VenueService(VenueServiceBase):
    id: int

    class Config:
        orm_mode = True


# ============= Модели для бронирований =============

class BookingBase(BaseModel):
    user_id: int
    venue_id: int
    time_slot_id: int

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: Optional[str] = None  # created, paid, cancelled
    total_price: Optional[float] = None

class Booking(BookingBase):
    id: int
    booking_date: datetime
    status: str
    total_price: float

    class Config:
        orm_mode = True

class BookingService(BaseModel):
    id: int
    booking_id: int
    service_id: int

    class Config:
        orm_mode = True


# ============= Модели для команд =============

class TeamBase(BaseModel):
    name: str
    sport_category_id: int
    creator_id: int
    capacity: int = 10
    logo_url: Optional[str] = None
    is_auto_team: bool = False
    event_id: Optional[int] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    sport_category_id: Optional[int] = None
    logo_url: Optional[str] = None
    capacity: Optional[int] = None
    current_members: Optional[int] = None
    is_auto_team: Optional[bool] = None
    event_id: Optional[int] = None

class Team(TeamBase):
    id: int
    current_members: int = 1

    class Config:
        orm_mode = True

class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    role: str = "player"  # captain, player
    position: Optional[str] = None

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    role: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None  # active, penalty, yellow card

class TeamMember(TeamMemberBase):
    id: int
    status: str = "active"
    join_date: datetime

    class Config:
        orm_mode = True

class TeamRequestBase(BaseModel):
    team_id: int
    user_id: int

class TeamRequestCreate(TeamRequestBase):
    pass

class TeamRequestUpdate(BaseModel):
    status: str  # pending, accepted, rejected

class TeamRequest(TeamRequestBase):
    id: int
    status: str = "pending"
    request_date: datetime

    class Config:
        orm_mode = True

class TeamStatsBase(BaseModel):
    team_id: int
    matches_played: int = 0
    wins: int = 0
    win_percentage: float = 0.0
    goals_scored: int = 0

class TeamStatsCreate(TeamStatsBase):
    pass

class TeamStatsUpdate(BaseModel):
    matches_played: Optional[int] = None
    wins: Optional[int] = None
    win_percentage: Optional[float] = None
    goals_scored: Optional[int] = None

class TeamStats(TeamStatsBase):
    id: int

    class Config:
        orm_mode = True

class EventTeamRegistrationBase(BaseModel):
    event_id: int
    team_id: int
    individual_fee: float = 0.0
    team_fee: float = 0.0

class EventTeamRegistrationCreate(EventTeamRegistrationBase):
    pass

class EventTeamRegistrationUpdate(BaseModel):
    status: Optional[str] = None  # pending, approved, rejected
    individual_fee: Optional[float] = None
    team_fee: Optional[float] = None
    payment_status: Optional[str] = None  # pending, paid

class EventTeamRegistration(EventTeamRegistrationBase):
    id: int
    registration_date: datetime
    status: str = "pending"
    payment_status: str = "pending"

    class Config:
        orm_mode = True