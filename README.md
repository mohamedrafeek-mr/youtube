# DjangoTube

A YouTube clone built using only Django (based on a blueprint).

## Tech Stack
- Backend: Django
- Database: SQLite (development) / PostgreSQL (production)
- Frontend: Django Templates + Bootstrap
- Media Storage: local (dev)

## Apps
- users
- videos
- comments
- interactions
- playlists
- search
- core

## Getting Started

1. Create a virtual environment and install Django.
   ```sh
   python -m venv venv
   venv\Scripts\activate
   pip install django
   ```
2. Add the apps to `INSTALLED_APPS` (already configured).
3. Run migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
5. Run server:
   ```sh
   python manage.py runserver
   ```

## Next Steps
- Implement forms and authentication flows
- Add FFmpeg processing for uploads
- Integrate Celery for background tasks
- Expand templates and static files

Refer to the blueprint in the project documentation for guidance.
