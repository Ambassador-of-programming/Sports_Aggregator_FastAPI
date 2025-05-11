from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


# Раздел категорий спорта
class SportCategory(Base):
    __tablename__ = 'sport_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon_url = Column(String)
    
    # Отношения
    feed_items = relationship("FeedItem", back_populates="category")
    events = relationship("Event", back_populates="sport_category")
    venues = relationship("Venue", back_populates="sport_category")
    teams = relationship("Team", back_populates="sport_category")

# Раздел Лента
class FeedItem(Base):
    __tablename__ = 'feed_items'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey('sport_categories.id'))
    is_interesting = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    # Отношения
    category = relationship("SportCategory", back_populates="feed_items")
    likes = relationship("FeedLike", back_populates="feed_item")

class FeedLike(Base):
    __tablename__ = 'feed_likes'
    
    id = Column(Integer, primary_key=True)
    feed_item_id = Column(Integer, ForeignKey('feed_items.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    feed_item = relationship("FeedItem", back_populates="likes")
    user = relationship("User", back_populates="feed_likes")

# Раздел мероприятия
class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    sport_category_id = Column(Integer, ForeignKey('sport_categories.id'))
    event_date = Column(DateTime, nullable=False)
    registration_end_date = Column(DateTime)
    price = Column(Float, default=0)
    available_seats = Column(Integer, default=0)
    total_seats = Column(Integer, default=0)
    location = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    competition_rules = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='new')  # new, active, completed
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    # Отношения
    sport_category = relationship("SportCategory", back_populates="events")
    owner = relationship("User", back_populates="owned_events")
    registrations = relationship("EventRegistration", back_populates="event")
    likes = relationship("EventLike", back_populates="event")
    teams = relationship("Team", back_populates="event")
    team_registrations = relationship("EventTeamRegistration", back_populates="event")

class EventLike(Base):
    __tablename__ = 'event_likes'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    event = relationship("Event", back_populates="likes")
    user = relationship("User", back_populates="event_likes")

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')  # pending, approved, rejected
    
    # Отношения
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="event_registrations")

# Раздел площадок
class Venue(Base):
    __tablename__ = 'venues'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    address = Column(String)
    image_url = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    venue_type = Column(String)
    sport_category_id = Column(Integer, ForeignKey('sport_categories.id'))
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    # Отношения
    owner = relationship("User", back_populates="owned_venues")
    sport_category = relationship("SportCategory", back_populates="venues")
    time_slots = relationship("TimeSlot", back_populates="venue")
    services = relationship("VenueService", back_populates="venue")
    bookings = relationship("Booking", back_populates="venue")
    likes = relationship("VenueLike", back_populates="venue")

class VenueLike(Base):
    __tablename__ = 'venue_likes'
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    venue = relationship("Venue", back_populates="likes")
    user = relationship("User", back_populates="venue_likes")

class TimeSlot(Base):
    __tablename__ = 'time_slots'
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    date = Column(DateTime)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Отношения
    venue = relationship("Venue", back_populates="time_slots")
    bookings = relationship("Booking", back_populates="time_slot")

class VenueService(Base):
    __tablename__ = 'venue_services'
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    
    # Отношения
    venue = relationship("Venue", back_populates="services")
    booking_services = relationship("BookingService", back_populates="service")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    time_slot_id = Column(Integer, ForeignKey('time_slots.id'))
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='created')  # created, paid, cancelled
    total_price = Column(Float, default=0)

    # Отношения
    user = relationship("User", back_populates="bookings")
    venue = relationship("Venue", back_populates="bookings")
    time_slot = relationship("TimeSlot", back_populates="bookings")
    booking_services = relationship("BookingService", back_populates="booking")

class BookingService(Base):
    __tablename__ = 'booking_services'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    service_id = Column(Integer, ForeignKey('venue_services.id'))

    # Отношения
    booking = relationship("Booking", back_populates="booking_services")
    service = relationship("VenueService", back_populates="booking_services")

# Раздел профиля и пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    avatar_url = Column(String)
    followers_count = Column(Integer, default=0)
    reviews_count = Column(Integer, default=0)

    # Отношения
    owned_events = relationship("Event", back_populates="owner")
    owned_venues = relationship("Venue", back_populates="owner")
    event_registrations = relationship("EventRegistration", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    feed_likes = relationship("FeedLike", back_populates="user")
    event_likes = relationship("EventLike", back_populates="user")
    venue_likes = relationship("VenueLike", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")
    team_requests = relationship("TeamRequest", back_populates="user")
    created_teams = relationship("Team", back_populates="creator")

# Раздел команд
class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sport_category_id = Column(Integer, ForeignKey('sport_categories.id'))
    logo_url = Column(String)
    capacity = Column(Integer, default=0)
    current_members = Column(Integer, default=0)
    is_auto_team = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'), nullable=True)
    
    # Отношения
    sport_category = relationship("SportCategory", back_populates="teams")
    creator = relationship("User", back_populates="created_teams")
    event = relationship("Event", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")
    requests = relationship("TeamRequest", back_populates="team")
    stats = relationship("TeamStats", back_populates="team", uselist=False)
    event_registrations = relationship("EventTeamRegistration", back_populates="team")

class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(String, default='player')  # captain, player
    position = Column(String)  # forward, defender, etc.
    status = Column(String, default='active')  # active, penalty, yellow card
    join_date = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")

class TeamRequest(Base):
    __tablename__ = 'team_requests'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='pending')  # pending, accepted, rejected
    request_date = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    team = relationship("Team", back_populates="requests")
    user = relationship("User", back_populates="team_requests")

class TeamStats(Base):
    __tablename__ = 'team_stats'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    win_percentage = Column(Float, default=0)
    goals_scored = Column(Integer, default=0)
    
    # Отношения
    team = relationship("Team", back_populates="stats")

class EventTeamRegistration(Base):
    __tablename__ = 'event_team_registrations'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')  # pending, approved, rejected
    individual_fee = Column(Float, default=0)
    team_fee = Column(Float, default=0)
    payment_status = Column(String, default='pending')  # pending, paid
    
    # Отношения
    event = relationship("Event", back_populates="team_registrations")
    team = relationship("Team", back_populates="event_registrations")