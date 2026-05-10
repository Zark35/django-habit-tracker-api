# Habit Tracker API

Backend REST API for habit tracking built with Django REST Framework.

## Description

This is a professional backend API designed to manage habits, record daily tracking, and provide secure authentication via JWT. The project is ready to run with Docker, PostgreSQL, and Redis.

## Technologies

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Docker
- JWT Authentication
- Swagger / OpenAPI

## Features

- JWT Authentication
- CRUD operations for habits
- Daily habit tracking
- Dockerized setup
- PostgreSQL integration
- Swagger/OpenAPI documentation
- Modular architecture

## Project Structure

- `apps/` - Functional Django applications
- `core/` - Shared utilities and configurations
- `habit_tracker/` - Main Django configuration
- `manage.py` - Django management commands
- `Dockerfile` - Docker image for the app
- `docker-compose.yml` - Docker orchestration
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables example

## Local Installation

1. Copy the environment variables file:

```bash
cp .env.example .env
```

2. Start services with Docker:

```bash
docker-compose up --build
```

3. Run migrations:

```bash
docker-compose run --rm web python manage.py migrate
```

4. Create superuser:

```bash
docker-compose run --rm web python manage.py createsuperuser
```

## Authentication and Token Usage

1. Open the interactive API documentation:

   ```bash
   http://localhost:8000/api/docs/
   ```

2. Locate the `POST /api/auth/login/` endpoint.
3. Click `Try it out` and replace the request body with your credentials:

   ```json
   {
     "email": "admin@example.com",
     "password": "admin123"
   }
   ```

4. Click `Execute`.
5. Copy the `access` token from the response, for example:

   ```json
   {
     "message": "Login successful.",
     "user": { ... },
     "tokens": {
       "access": "<access_token>",
       "refresh": "<refresh_token>"
     }
   }
   ```

6. In Swagger UI, click the `Authorize` button and paste:

   ```text
   Bearer <access_token>
   ```

7. After authorization, Swagger will send the token automatically to protected endpoints.

8. You can also use the access token directly in requests by adding the header:

   ```http
   Authorization: Bearer <access_token>
   ```

### What to do with the token

- Use it to call protected endpoints like:
  - `GET /api/habits/`
  - `POST /api/habits/`
  - `GET /api/tracking/`
  - `POST /api/tracking/`
  - `GET /api/auth/profile/me/`

- If the access token expires, refresh it at:
  - `POST /api/auth/refresh_token/`

- You can also use the token in Postman or Insomnia for authenticated requests.

## Environment Variables

- `SECRET_KEY` - Django secret key
- `DB_NAME` - PostgreSQL database name
- `DB_USER` - PostgreSQL user
- `DB_PASSWORD` - PostgreSQL password
- `DB_HOST` - Database host
- `DB_PORT` - PostgreSQL port
- `JWT_SECRET_KEY` - JWT secret key
- `REDIS_URL` - Redis URL
- `CORS_ALLOWED_ORIGINS` - Allowed origins

## Main Endpoints

- `/api/auth/register/` - Register a new user
- `/api/auth/login/` - Login and obtain JWT tokens
- `/api/auth/refresh_token/` - Refresh access token
- `/api/auth/profile/me/` - Current user profile
- `/api/habits/` - Habit management
- `/api/tracking/` - Daily tracking entries
- `/api/` - API root view (lists available endpoints)
- `/api/docs/` - Interactive API documentation (Swagger UI)
- `/api/schema/` - OpenAPI schema (JSON download for API documentation)

## Project Status

- ✅ Functional
- ✅ Docker compatible
- ✅ PostgreSQL integrated
- ✅ Redis integrated
- ✅ Swagger documentation available
- ✅ Clean and modular structure

## Future Improvements

- Add unit and integration tests
- Add analytics and metrics endpoints
- Implement advanced roles and permissions
- Deploy with CI/CD
- Add notification use cases

## Author

Developed by Andrés Bohórquez

- GitHub: https://github.com/Zark35
- LinkedIn: www.linkedin.com/in/andrés-bohórquez-5b2a55340
