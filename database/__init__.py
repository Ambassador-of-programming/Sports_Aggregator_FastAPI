# database/__init__.py
from .base import Base, engine, SessionLocal, get_db
from .models import (SportCategory, FeedItem, FeedLike, Event, EventLike, 
                    EventRegistration, Venue, VenueLike, TimeSlot, VenueService, 
                    Booking, BookingService, User, Team, TeamMember, TeamRequest, 
                    TeamStats, EventTeamRegistration)

def create_tables():
    Base.metadata.create_all(bind=engine)