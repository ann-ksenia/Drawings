import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from room.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        room = Room.objects.get(name=self.room_name)
        status = User.objects.get(room=room, name=self.username).status
        if status == 'Creator':
            room.delete()
    # def receive_json(self, content, **kwargs):
    #     type = content["type"]
    #     username = content["username"]
    #     if type == "onclose":
    #         room = User.objects.get(name=username).room
    #         for i in User.objects.filter(room = room):
    #             i.delete()
    #         room.delete()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        self.username = text_data_json['username']
        username = text_data_json['username']


        if type == "chat":
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username':username,
                }
            )
        if type == "change_status":
            status = text_data_json['status']
            room = Room.objects.get(name = self.room_name)
            user = User.objects.get(room = room, name = username)
            user.status=status
            user.save()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username':username,
        }))
