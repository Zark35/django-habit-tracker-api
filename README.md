# Habit Tracker API

Backend REST API para seguimiento de hábitos construida con Django REST Framework.

## Descripción

Esta es una API backend profesional diseñada para administrar hábitos, registrar seguimiento diario y proveer autenticación segura mediante JWT. El proyecto está preparado para ejecutarse con Docker, PostgreSQL y Redis.

## Tecnologías

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Docker
- JWT Authentication
- Swagger / OpenAPI

## Características

- JWT Authentication
- CRUD de hábitos
- Seguimiento de hábitos diarios
- Dockerized setup
- Integración con PostgreSQL
- Documentación Swagger/OpenAPI
- Arquitectura modular

## Estructura del proyecto

- `apps/` - Aplicaciones Django funcionales
- `core/` - Utilities y configuraciones compartidas
- `habit_tracker/` - Configuración principal de Django
- `manage.py` - Comandos Django
- `Dockerfile` - Imagen Docker para la app
- `docker-compose.yml` - Orquestación Docker
- `requirements.txt` - Dependencias Python
- `.env.example` - Ejemplo de variables de entorno

## Instalación local

1. Copiar el archivo de variables de entorno:

```bash
cp .env.example .env
```

2. Iniciar los servicios con Docker:

```bash
docker-compose up --build
```

3. Ejecutar migraciones:

```bash
docker-compose run --rm web python manage.py migrate
```

4. Crear superusuario:

```bash
docker-compose run --rm web python manage.py createsuperuser
```

## Variables de entorno

- `SECRET_KEY` - Clave secreta de Django
- `DB_NAME` - Nombre de la base de datos PostgreSQL
- `DB_USER` - Usuario de PostgreSQL
- `DB_PASSWORD` - Contraseña de PostgreSQL
- `DB_HOST` - Host de la base de datos
- `DB_PORT` - Puerto de PostgreSQL
- `JWT_SECRET_KEY` - Clave JWT
- `REDIS_URL` - URL de Redis
- `CORS_ALLOWED_ORIGINS` - Orígenes permitidos

## Endpoints principales

- `/api/auth/`
- `/api/habits/`
- `/api/tracking/`
- `/api/docs/`

## Estado del proyecto

- ? Funcional
- ? Docker compatible
- ? PostgreSQL integrado
- ? Redis integrado
- ? Documentación Swagger disponible
- ? Estructura limpia y modular

## Posibles mejoras futuras

- Agregar pruebas unitarias e integración
- Añadir endpoints analíticos y métricas
- Implementar roles y permisos avanzados
- Desplegar con CI/CD
- Añadir casos de uso para notificaciones

## Autor

- GitHub: https://github.com/Zark35
