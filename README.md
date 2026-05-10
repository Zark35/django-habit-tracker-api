# Habit Tracker API

Backend REST API para seguimiento de h�bitos construida con Django REST Framework.

## Descripci�n

Esta es una API backend profesional dise�ada para administrar h�bitos, registrar seguimiento diario y proveer autenticaci�n segura mediante JWT. El proyecto est� preparado para ejecutarse con Docker, PostgreSQL y Redis.

## Tecnolog�as

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Docker
- JWT Authentication
- Swagger / OpenAPI

## Caracter�sticas

- JWT Authentication
- CRUD de h�bitos
- Seguimiento de h�bitos diarios
- Dockerized setup
- Integraci�n con PostgreSQL
- Documentaci�n Swagger/OpenAPI
- Arquitectura modular

## Estructura del proyecto

- `apps/` - Aplicaciones Django funcionales
- `core/` - Utilities y configuraciones compartidas
- `habit_tracker/` - Configuraci�n principal de Django
- `manage.py` - Comandos Django
- `Dockerfile` - Imagen Docker para la app
- `docker-compose.yml` - Orquestaci�n Docker
- `requirements.txt` - Dependencias Python
- `.env.example` - Ejemplo de variables de entorno

## Instalaci�n local

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
- `DB_PASSWORD` - Contrase�a de PostgreSQL
- `DB_HOST` - Host de la base de datos
- `DB_PORT` - Puerto de PostgreSQL
- `JWT_SECRET_KEY` - Clave JWT
- `REDIS_URL` - URL de Redis
- `CORS_ALLOWED_ORIGINS` - Or�genes permitidos

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
- ? Documentaci�n Swagger disponible
- ? Estructura limpia y modular

## Posibles mejoras futuras

- Agregar pruebas unitarias e integraci�n
- A�adir endpoints anal�ticos y m�tricas
- Implementar roles y permisos avanzados
- Desplegar con CI/CD
- A�adir casos de uso para notificaciones

## Autor

Developed by Andrés Bohórquez

- GitHub: https://github.com/Zark35
- LinkedIn: www.linkedin.com/in/andrés-bohórquez-5b2a55340
