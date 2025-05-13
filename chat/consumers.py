import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Thread, Message
from django.contrib.auth.models import User
from django.db.models import Count
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # print()
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group


        friend = User.objects.get(id=self.room_name)     
        thread = self.get_or_create_thread(friend=friend)
        self.room_group_name = f"chat_{thread.id}"
        async_to_sync(self.channel_layer.group_add)(
             self.room_group_name, self.channel_name
        )
        self.accept() 

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def get_thread(self):
        return Thread.objects.annotate(num_users=Count('users')).filter(thread_type='PSN', users=self.scope["user"]).filter(users=self.room_name,num_users=2
).first()
    
    def get_or_create_thread(self, friend):
        thread = (Thread.objects
    .filter(thread_type='PSN', users__in=[self.scope["user"], friend])
    .annotate(num_users=Count('users'))
    .filter(num_users=2)
    .first()
)
        if not thread:
            thread = Thread.objects.create(thread_type='PSN')
            thread.users.add(self.scope["user"], friend)
        return thread
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        thread = self.get_thread()
        thread_message =  Message(thread=thread,content=message, sender=self.scope["user"])
        thread_message.save()
        thread.last_message = thread_message
        thread.save()
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "message_id": thread_message.id}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        message_id = event['message_id']
        user_message = Message.objects.get(id=message_id)
        # thread = 
        # mark as read if user is authenticated user
        if self.scope["user"] != user_message.sender:
            user_message.read = True
            user_message.save()
        
        # Send message to WebSocket 
        self.send(text_data=json.dumps({"message": message}))
