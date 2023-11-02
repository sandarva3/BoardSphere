import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Post, Topic

User = get_user_model()

class FirstConsumer(AsyncWebsocketConsumer):
    connected_clients = []

    async def connect(self):
        await self.accept()
        self.connected_clients.append(self)

    async def disconnect(self, close_code):
        self.connected_clients.remove(self)

    async def receive(self, text_data): 
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        topicName = text_data_json['topic']

        # Save the new message to the database
        new_message = await self.save_message(message, username, topicName)

        # Prepare the message data
        message_data = json.dumps({
            'message': new_message.message,
            'username': new_message.created_by.username,
            'timestamp': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            # ... any other data you want to send back ...
        })

        # Send the new message back to all connected clients
        for client in self.connected_clients:
            await client.send(text_data=message_data)

    @database_sync_to_async
    def save_message(self, message, username, topicName):
        user = User.objects.get(username=username)
        topic = Topic.objects.get(subject=topicName)
        new_message = Post.objects.create(message=message, created_by=user, topic=topic)
        return new_message
