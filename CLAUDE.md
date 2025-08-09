# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered image manipulation web application built with Django REST API backend and Vue.js frontend. The application allows users to generate images from text prompts using Stability AI, perform various image processing tasks (background removal, resizing, enhancement, etc.), and manage user accounts with a credit-based pricing system.

## Architecture

### Backend (Django 4.2+)
- **Main Apps**: `images`, `users`, `api`, `config`
- **Custom User Model**: `users.CustomUser` with email-based authentication
- **Database**: PostgreSQL with custom models for Image, Service, Credit, FeatureFlag, BaredUser
- **Authentication**: JWT tokens via `djangorestframework-simplejwt` with Google OAuth support
- **Task Queue**: Celery with Redis broker for asynchronous image processing
- **Cloud Integration**: AWS S3 for production storage, Lambda for processing
- **Payment**: Stripe integration with credit system (1$ = 50 credits)

### Frontend (Vue 3)
- **Framework**: Vue 3 with Vue Router 4
- **Styling**: Tailwind CSS 4.x
- **API Communication**: RESTful calls to Django backend at `http://localhost:8084`
- **Development Server**: Runs on port 5000

### Infrastructure
- **Containerization**: Docker Compose with separate services
- **Services**: Django (8084), Vue.js (5000), PostgreSQL, Redis, Celery Worker
- **Message Broker**: Redis on port 6380 (mapped from 6379)

## Development Commands

### Starting the Application
```bash
# Full development environment
docker-compose up --build

# Individual services
cd imageassistant/frontend && npm run serve  # Frontend only
cd imageassistant && python manage.py runserver 8084  # Backend only
celery -A config worker --loglevel=info  # Celery worker
```

### Frontend Development
```bash
cd imageassistant/frontend
npm install
npm run serve    # Development server
npm run build    # Production build
npm run lint     # ESLint
```

### Backend Development
```bash
cd imageassistant
python manage.py runserver 8084
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### CSS Processing
```bash
# Tailwind CSS compilation (from project root)
npx @tailwindcss/cli -i ./imageassistant/assets/css/input.css -o ./imageassistant/assets/css/tailwind.css --watch

# For Vue frontend specifically
npx @tailwindcss/cli -i ./imageassistant/assets/css/input.css -o ./imageassistant/frontend/src/styles/css/tailwind.css --watch
```

### Container Management
```bash
# Execute commands in containers
./container-command.sh imageassistant_django_1 "python manage.py migrate"
./container-command.sh imageassistant_django_1 "sh"  # Shell access

# Set proper permissions
CURRENT_UID=$(id -u):$(id -g) docker-compose up
```

## Key Configuration Files

### Environment Variables
- Location: `imageassistant/.env`
- Required: `SECRET_KEY`, `DB_*`, `REDIS_URL`, `CELERY_*`
- Optional: `STRIPE_*`, `STABILITY_AI_KEY`, `GOOGLE_CLIENT_ID`, `AWS_*`

### Settings
- Development: `config.settings`
- Production: `config.production_settings`
- Key settings: Custom user model, JWT configuration, CORS, Celery, S3 storage

### Database Models
- **Image**: Main model for uploaded/generated images with processing status
- **Service**: Dynamic service definitions with token costs
- **CustomUser**: Email-based authentication with Google OAuth
- **Credit**: One-to-one with users for billing
- **FeatureFlag**: Per-user or global feature toggles
- **BaredUser**: Account banning system

## API Architecture

### Authentication Endpoints
- `POST /api/v1/custom/token/obtain/` - Login
- `POST /api/v1/google/login/` - Google OAuth
- `POST /api/v1/users/signup/` - Registration
- `GET /api/v1/user/info/` - User profile and credits

### Image Processing Endpoints
- `POST /api/v1/create/image/from/prompt/` - AI image generation
- `GET /api/v1/image/status/<id>/` - Processing status polling
- `PUT /api/v1/update/processed/image/<id>/` - Update processed image

### URL Configuration
- Main URLs: `config.urls`
- App URLs: `images.urls`, `users.urls`, `api.urls`
- JWT token endpoints at `/api/v1/token/`

## Development Patterns

### JWT Authentication
- Tokens in Authorization header: `Bearer <token>`
- 1-day lifetime for both access and refresh tokens
- Automatic token refresh on frontend

### Async Processing
- Celery tasks in `images.tasks`
- Status polling pattern for long-running operations
- Redis as message broker and result backend

### Feature Flags
- Dynamic feature toggles per user or globally
- Check with `FeatureFlag.is_active_for(user)`
- Template tag: `{% feature_flag 'flag_name' user %}`

### Credit System
- 1$ = 50 credits (configurable via `CREDIT_SETTINGS`)
- Service costs defined in Service model
- Automatic deduction on image processing

## Common Tasks

### Adding New Image Processing Service
1. Add service to `services` choices in `images.models`
2. Create migration: `python manage.py makemigrations`
3. Add processing logic to `images.tasks`
4. Update API endpoints in `api.views`
5. Add frontend components for the service

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations  # Check status
```

### Static Files
- Collect: `python manage.py collectstatic`
- CSS compilation handled by Tailwind CLI
- Vue.js assets built separately with `npm run build`

### Testing
- Backend tests in each app's `tests.py`
- No test runner configured - add test commands as needed
- Frontend linting: `npm run lint`

## Security Features
- CSRF protection on all forms
- Custom user model with email authentication
- Account banning system via BaredUser model
- Feature flags for controlled rollouts
- AWS S3 integration with proper IAM policies
- Google OAuth for secure authentication

## Production Considerations
- Set `DEBUG = False` in production settings
- Configure AWS S3 for file storage
- Use environment variables for all secrets
- Set up proper CORS and ALLOWED_HOSTS
- Configure SSL/TLS termination
- Set up monitoring for Celery workers