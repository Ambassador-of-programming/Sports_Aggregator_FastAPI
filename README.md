# Sports Aggregator Backend

<div align="center">
  <img src="icon.png" alt="Sports Aggregator Logo" width="200">
</div>

## Overview

Sports Aggregator is a comprehensive platform designed to connect sports enthusiasts by providing tools for event organization, venue booking, team management, and a sporting community feed. This repository contains the FastAPI-based backend service that powers the Sports Aggregator platform.

## Related Projects

- **Mobile Application**: [Sports_Aggregator_MobileApp_Flet](https://github.com/Ambassador-of-programming/Sports_Aggregator_MobileApp_Flet)

## Technology Stack

- **Framework**: FastAPI
- **Python Version**: 3.11.4
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **Dependency Management**: Pipenv

## Features

- **Sports Categories Management**: Organize events and venues by sport type
- **Event System**: Create, join and manage sporting events
- **Venue Booking**: Find and book sports facilities with available time slots
- **Team Management**: Create teams, manage membership and track statistics
- **User Profiles**: Handle user registration, authentication and profiles
- **Interactive Feed**: Community engagement with likes and views tracking
- **Booking Services**: Comprehensive system for venue reservations

## Project Structure

- **base.py**: Database connection setup and session management
- **models.py**: SQLAlchemy ORM models defining the database schema
- **main.py**: Application entry point with route registration
- **routes/**: API endpoints organized by resource
- **docker-compose.yml**: Multi-container Docker setup
- **nginx.conf**: Reverse proxy configuration
- **other**: other files and folders

## Database Schema

The application uses a PostgreSQL database with the following key entities:

- **SportCategory**: Different types of sports
- **User**: User account information
- **Event**: Sporting events with registrations
- **Venue**: Sports facilities with booking capabilities 
- **Team**: Groups of users participating in events
- **FeedItem**: Community content and interactions

## Installation & Setup

### Prerequisites

- Python 3.11.4
- Docker and Docker Compose
- Pipenv

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Ambassador-of-programming/Sports_Aggregator_FastAPI.git
   cd Sports_Aggregator_FastAPI
   ```

2. Set up the virtual environment:
   ```bash
   pipenv install
   pipenv shell
   ```

3. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. The API will be available at http://localhost:8000 and through Nginx at http://localhost:80

### Environment Variables

The application uses the following environment variables:
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request