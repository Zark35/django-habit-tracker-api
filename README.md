# Habit Tracker API

![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-4.2.13-092E20)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Zark35/django-habit-tracker-api/actions/workflows/tests.yml/badge.svg)

## Overview

Habit Tracker API is a backend-first REST API for mobile habit tracking and productivity apps. The service delivers secure JWT authentication, habit lifecycle management, daily tracking, Redis-backed caching/broker support, and OpenAPI documentation.

---

## Architecture

```text
Mobile Client / Frontend
          ↓
   Django REST API
       /      \
 PostgreSQL   Redis
                 │
               Celery
```

- **Django REST API**: API layer, business rules, and authorization
- **PostgreSQL**: persistent storage for users, habits, and entries
- **Redis**: cache and background task broker
- **Celery**: asynchronous task processing architecture

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2.13, Django REST Framework 3.14.0 |
| Database | PostgreSQL 15 |
| Authentication | JWT via djangorestframework-simplejwt |
| API Docs | drf-spectacular, Swagger, ReDoc |
| Infrastructure | Docker, docker-compose |
| Cache / Broker | Redis 7 |
| Task Queue | Celery 5.3.6 |
| Testing | pytest, pytest-django, factory-boy |

---

## Features

- ✅ JWT authentication with access and refresh tokens
- ✅ Habit CRUD and validation
- ✅ Daily habit tracking entries
- ✅ Dockerized local development
- ✅ Swagger/OpenAPI documentation
- ✅ Redis integration for cache and task queue
- ✅ Celery support for async processing
- ✅ Modular Django app architecture

---

## Repository Structure

```text
.
├── .github/                  # CI workflows
├── apps/                     # Django application modules
│   ├── habits/               # Habit feature domain
│   ├── tracking/             # Habit entry tracking domain
│   └── users/                # Authentication and user APIs
├── core/                     # Shared utilities and custom exceptions
├── habit_tracker/            # Django project configuration
├── docker-compose.yml        # Local orchestration
├── Dockerfile                # Container build configuration
├── requirements.txt          # Dependencies
├── .env.example              # Environment variable template
└── README.md                 # Project documentation
```

---

## Local Setup

### 1. Clone repository

```bash
git clone https://github.com/Zark35/django-habit-tracker-api.git
cd django-habit-tracker-api
```

### 2. Copy environment file

```bash
cp .env.example .env
```

### 3. Start containers

```bash
docker-compose up --build
```

### 4. Apply database migrations

```bash
docker-compose run --rm web python manage.py migrate
```

### 5. Create a superuser

```bash
docker-compose run --rm web python manage.py createsuperuser
```

### 6. Access local services

- API root: `http://localhost:8000/api/`
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

---

## Environment Variables

The project uses `.env` for local configuration. Key variables:

| Variable | Description |
|---|---|
| `DEBUG` | Enable Django debug mode |
| `DJANGO_SETTINGS_MODULE` | Django settings module |
| `SECRET_KEY` | Django application secret |
| `ALLOWED_HOSTS` | Allowed hostnames |
| `DB_ENGINE` | Database backend |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `JWT_SECRET_KEY` | JWT signing key |
| `JWT_ALGORITHM` | JWT algorithm |
| `JWT_EXPIRATION_HOURS` | Access token lifetime |
| `JWT_REFRESH_EXPIRATION_DAYS` | Refresh token lifetime |
| `REDIS_URL` | Redis connection URL |
| `CORS_ALLOWED_ORIGINS` | Accepted frontend origins |
| `EMAIL_BACKEND` | Django email backend for local dev |

---

## API Documentation

The project includes auto-generated API docs and schema endpoints.

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

### Example API endpoints

- `POST /api/auth/register/` — Create a new user
- `POST /api/auth/login/` — Authenticate and receive JWT tokens
- `POST /api/auth/refresh_token/` — Refresh access token
- `GET /api/auth/profile/me/` — Current user profile
- `GET /api/habits/` — List user habits
- `POST /api/habits/` — Create a new habit
- `GET /api/tracking/` — List tracking entries
- `POST /api/tracking/` — Record a completed habit entry

---

## Authentication Flow

1. Create an account or use the superuser.
2. Login at `POST /api/auth/login/`.
3. Copy the returned `access` token.
4. Authorize Swagger with `Bearer <access_token>`.
5. Use protected endpoints with the `Authorization` header.

```http
Authorization: Bearer <access_token>
```

---

## Testing

Run tests inside Docker:

```bash
docker-compose run --rm web python -m pytest -q
```

If dependencies change, rebuild first:

```bash
docker-compose build --no-cache web
```

Reuse the test database for faster feedback:

```bash
docker-compose run --rm web python -m pytest --reuse-db
```

---

## CI / CD

The repository includes GitHub Actions workflows for:

- automated test execution
- linting and quality validation
- Docker packaging

CI status is surfaced in the README badge.

---

## Roadmap

- Add full unit and integration coverage
- Implement role-based authorization
- Add analytics and reporting endpoints
- Deploy to Render / AWS / Kubernetes
- Add request rate limiting and caching policies
- Add email notifications and reminders

---

## Screenshots

![Swagger UI placeholder](./docs/swagger-ui-placeholder.png)
![API docs placeholder](./docs/api-docs-placeholder.png)

---

## Deployment

This backend is ready for future deployment to platforms such as:

- Render
- AWS Elastic Beanstalk
- AWS ECS / EKS
- DigitalOcean App Platform

Deployment should use environment variables and managed PostgreSQL / Redis services.

### Live deployment
- The application is deployed in Render: https://django-habit-tracker-api.onrender.com
- Public Swagger UI: https://django-habit-tracker-api.onrender.com/api/docs/#/auth/auth_login_create

---

## Contributing

Contributions are welcome. Please use the standard workflow:

1. Fork the repository
2. Create a feature branch
3. Add tests for new behavior
4. Submit a pull request with a clear summary

Please keep changes modular and preserve existing API contracts.

---

## License

This project is released under the MIT License.

---

## Author

Developed by Andrés Bohórquez

- GitHub: https://github.com/Zark35
- LinkedIn: www.linkedin.com/in/andrés-bohórquez-5b2a55340
- Public Swagger UI: https://django-habit-tracker-api.onrender.com/api/docs/#/auth/auth_login_create
