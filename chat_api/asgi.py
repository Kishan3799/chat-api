"""
ASGI config for chat_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://djangoproject.com
"""

import os
import django
from django.core.asgi import get_asgi_application

# 1. Set the environment variable first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')

# 2. Initialize Django and the base HTTP ASGI application immediately
django.setup()
django_asgi_app = get_asgi_application()

# 3. Import Channels and routing components ONLY after Django is setup
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# 4. Define the protocol router application
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
