# Real-time Chat API

Django Channels + WebSockets real-time chat application.

## Features
- Real-time messaging via WebSockets
- REST API for rooms and message history
- User authentication

## Tech Stack
Django, Django Channels, Daphne, Django REST Framework

## Run Locally
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit: `/chat/<room_name>/`