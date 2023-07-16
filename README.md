# Kanban Like Backend for Interview Applications

Contains:

API Level

1. User Registiration
1. User Authentication (with JWT)
1. Categories (CRUD)
1. Boards (CRUD)

Websocket Level

1. Time
1. Notifications
1. Changes

Contained Technologies

1. [Django](https://www.djangoproject.com/)
1. [Rest Framework](https://www.djangoproject.com/)
1. [Json Web Token](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
1. [Daphne Serving for ASGI](https://channels.readthedocs.io/en/stable/deploying.html)
1. [SQLite for Database](https://www.sqlite.org/index.html)

Setup

```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
$ python manage.py runserver <ip_address:desired_port>
```