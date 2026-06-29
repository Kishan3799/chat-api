from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import ChatRoomViewSet, RoomMessagesView

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='chatroom')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/messages/<str:room_name>/', RoomMessagesView.as_view(), name='room-messages'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]