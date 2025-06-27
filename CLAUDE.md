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

Since the project is in planning phase, these commands will be relevant once implementation begins:

### Python/Django Backend
```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Django management
python manage.py migrate
python manage.py runserver
python manage.py test
python manage.py collectstatic

# Celery (for background tasks)
celery -A healthquest worker --loglevel=info
```

### Frontend (when React is set up)
```bash
# Install dependencies
npm install

# Development
npm run dev
npm run build
npm run test
npm run lint
npm run type-check

# PWA build
npm run build:pwa
```

### Docker Development
```bash
# Build and run containers
docker-compose up --build
docker-compose down

# Run specific services
docker-compose up postgres redis
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

### Data Models (Planned)
Key Django models will include:
- `User` (extended Django user)
- `Character` (user's RPG character with 8 stats)
- `Quest` (individual tasks/challenges)
- `QuestCompletion` (tracking user progress)
- `Guild` (team/group functionality)
- `Reward` (experience, gold, gems, titles, skins)

## Development Phases

### Phase 1 (Weeks 1-2): Infrastructure & Core Backend
- Django project setup with Docker
- JWT authentication system
- Quest & stats model design
- Basic REST API CRUD operations

### Phase 2 (Weeks 3-4): Frontend Foundation
- React app architecture
- Component library setup
- Main dashboard implementation
- Quest completion functionality

### Phase 3 (Weeks 5-6): Advanced Features
- AI recommendation system prototype
- Guild system development
- Real-time notifications (WebSocket)
- Data visualization charts

### Phase 4 (Week 7): PWA & Mobile
- PWA configuration and offline support
- Responsive design completion
- Push notification implementation

### Phase 5 (Week 8): Testing & Deployment
- Unit and integration tests
- Performance optimization
- User acceptance testing
- Production deployment

## Key Implementation Notes

- The service targets Korean users initially (Korean language support required)
- Focus on gamification without being overwhelming
- Emphasize collaboration over competition in social features
- Privacy-first approach with user data ownership
- Freemium model with Premium (₩5,000/month) and Pro (₩9,000/month) tiers

## Testing Strategy

- Django: Use pytest-django for backend testing
- React: Jest and React Testing Library for frontend
- E2E: Playwright or Cypress for integration testing
- Performance: Load testing with locust for Django backend

## Deployment

- Containerized deployment using Docker
- CI/CD pipeline with GitHub Actions
- Database migrations handled through Django's migration system
- Static files served through CDN (AWS CloudFront or similar)