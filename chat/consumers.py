import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        """Called when WebSocket connects"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send last 20 messages on connect
        messages = await self.get_recent_messages()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages
        }))
    
    async def disconnect(self, close_code):
        """Called when WebSocket disconnects"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Called when message received from WebSocket"""
        data = json.loads(text_data)
        message = data.get('message', '')
        username = data.get('username', 'Anonymous')
        
        if not message.strip():
            return
        
        # Save message to database
        await self.save_message(username, message)
        
        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )
    
    async def chat_message(self, event):
        """Called when message received from room group"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
        }))
    
    @database_sync_to_async
    def save_message(self, username, content):
        try:
            room, _ = ChatRoom.objects.get_or_create(
                name=self.room_name,
                defaults={'created_by': User.objects.filter(username=username).first() or User.objects.first()}
            )
            user = User.objects.get(username=username)
            Message.objects.create(room=room, user=user, content=content)
        except Exception as e:
            print(f"Error saving message: {e}")
    
    @database_sync_to_async
    def get_recent_messages(self):
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            messages = Message.objects.filter(room=room).order_by('-timestamp')[:20]
            return [
                {
                    'username': msg.user.username,
                    'message': msg.content,
                    'timestamp': str(msg.timestamp)
                }
                for msg in reversed(list(messages))
            ]
        except ChatRoom.DoesNotExist:
            return []