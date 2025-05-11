from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import (booking, event, feed, sport_category, team, user, venue, database)
import uvicorn


app = FastAPI(debug=False)

# Register routes
app.include_router(user.user_router,  prefix="/users")
app.include_router(sport_category.sport_category_router, prefix="/sport-categories")
app.include_router(feed.feed_router, prefix="/feed")
app.include_router(event.event_router, prefix="/events")
app.include_router(venue.venue_router, prefix="/venues")
app.include_router(team.team_router, prefix="/teams")
app.include_router(booking.booking_router, prefix="/bookings")

app.include_router(database.database_router, prefix="/database")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, host="0.0.0.0")
