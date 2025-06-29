# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HealthQuest is a health management RPG web service that gamifies healthy lifestyle habits. The project is currently in the planning phase with a comprehensive roadmap defined in `HEALTHQUEST_IMPROVED_PLAN.md`.

## Planned Technology Stack

### Frontend
- **React 18** with **TypeScript** for type safety and maintainability
- **Tailwind CSS** for rapid styling
- **Framer Motion** for smooth animations
- **Chart.js** and **D3.js** for data visualization
- **PWA Workbox** for offline support

### Backend
- **Django 4.2** with **Django REST Framework**
- **PostgreSQL** as primary database
- **Redis** for caching and real-time features
- **Celery** for background tasks
- **TensorFlow Lite** for AI recommendation system

### Infrastructure
- **Docker** for containerization
- **AWS/GCP** for cloud deployment
- **GitHub Actions** for CI/CD
- **Sentry** for error monitoring

## Development Commands

The project is currently implemented as a Django backend with Docker containerization.

### Docker Development (Primary)
```bash
# Build and run all services
docker-compose up --build -d

# Check service status
docker-compose ps

# View logs
docker-compose logs web
docker-compose logs celery

# Django management commands (within container)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py collectstatic

# Create superuser
docker-compose exec web python manage.py shell -c "
from apps.accounts.models import User
User.objects.create_superuser(
    username='admin',
    email='admin@healthquest.com', 
    password='admin123',
    nickname='관리자'
)"

# Generate sample quest data
docker-compose exec web python manage.py create_sample_quests

# Stop services
docker-compose down
```

### Testing
```bash
# Run comprehensive API tests
python3 test_api.py

# Run Django unit tests
docker-compose exec web python manage.py test

# Test specific app
docker-compose exec web python manage.py test apps.characters
```

### Local Development (Alternative)
```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with local database (requires PostgreSQL and Redis)
python manage.py runserver

# Run Celery worker
celery -A healthquest worker --loglevel=info
```

## Core Architecture

### Character System
The application centers around an 8-stat character system:
- 체력 (Stamina) - Basic fitness and energy management
- 근력 (Strength) - Muscle and resistance training
- 정신력 (Mental) - Stress management and focus
- 지구력 (Endurance) - Cardio and persistence
- 심폐 (Cardio) - Cardiovascular health
- 유연성 (Flexibility) - Stretching and yoga
- 영양 (Nutrition) - Balanced diet
- 회복 (Recovery) - Sleep and rest

### Quest System
- AI-powered personalized quest recommendations
- Time-based categories (Morning, Work, Evening, Night, Weekly, Challenge)
- Difficulty auto-adjustment based on user patterns
- Weather and schedule integration

### Social Features
- Guild system (4-8 member teams)
- Friend system with quest sharing
- Real-time encouragement messaging
- Couple/family collaboration modes

### Data Models (Implemented)
Key Django models currently implemented:

**apps.accounts.models:**
- `User` (extended AbstractUser with health profile fields)
- `UserProfile` (additional profile settings and preferences)

**apps.characters.models:**
- `Character` (RPG character with 8-stat system and game currency)
- `Achievement` (system-wide achievements/titles)
- `UserAchievement` (user's earned achievements)
- `StatHistory` (tracks character stat changes over time)

**apps.quests.models:** (structure inferred from API endpoints)
- Quest system with difficulty levels and categories
- Quest completion tracking and streak mechanics

**apps.guilds.models:** (structure inferred from API endpoints)
- Guild creation and membership system
- Guild messaging and collaborative features

## Current Implementation Status

### ✅ Completed (Phase 1)
- Django 4.2 project setup with Docker containerization
- JWT authentication system using django-rest-framework-simplejwt
- Extended User model with health profile fields
- Complete 8-stat character system with experience/leveling
- Achievement system with categories and rewards
- Stat history tracking for progress visualization
- Basic REST API with comprehensive endpoints
- PostgreSQL database with Redis caching
- Celery background task system
- CORS configuration for frontend integration

### 🚧 In Progress
- Quest system implementation (models and API endpoints exist)
- Guild system with membership and messaging
- Sample data generation management command

### 📋 Next Development Phases

### Phase 2: Frontend Foundation
- React 18 + TypeScript application
- Component library with Tailwind CSS
- Main dashboard with character stats visualization
- Quest management interface

### Phase 3: Advanced Features  
- AI recommendation system for personalized quests
- Real-time notifications with WebSocket
- Advanced data visualization with Chart.js/D3.js
- Weather and calendar integration

### Phase 4: PWA & Mobile
- Progressive Web App configuration
- Offline support with service workers
- Push notifications
- Mobile-responsive design

### Phase 5: Production Ready
- Comprehensive testing suite
- Performance optimization
- Production deployment pipeline
- Monitoring and analytics

## Key Implementation Notes

- Custom User model extends AbstractUser with email as USERNAME_FIELD
- Character stats auto-level on experience gain with configurable distribution
- JWT tokens: 15min access, 7-day refresh with rotation
- Korean locale (Asia/Seoul timezone, ko-kr language)
- CORS configured for localhost:3000 frontend development
- Database uses PostgreSQL with custom table names
- All models include Korean verbose names for admin interface

## API Architecture

### Authentication Flow
1. Register → Auto-creates Character with default stats
2. Login → Returns JWT access/refresh token pair  
3. All API endpoints require Bearer token authentication
4. Character creation is automatic on user registration

### Character Progression System
- Experience gain triggers automatic level-up calculation
- Stats auto-distribute on level-up (2 points per level)
- Stat changes logged in StatHistory for analytics
- Achievement system tracks user progress milestones

### Service Architecture
- **web**: Django application server (port 8000)
- **db**: PostgreSQL 15 (port 5433)
- **redis**: Redis 7 for caching/sessions (port 6380)
- **celery**: Background task worker

## Testing Strategy

- **test_api.py**: Comprehensive integration tests covering full user journey
- Django TestCase for unit testing individual models/views
- API testing includes authentication, character creation, quest system
- Test data uses unique timestamps to avoid conflicts

## Database Schema

### Key Relationships
- User (1:1) Character
- User (1:1) UserProfile  
- Character (1:N) StatHistory
- User (M:N) Achievement through UserAchievement
- Character progression uses experience points with level-based scaling