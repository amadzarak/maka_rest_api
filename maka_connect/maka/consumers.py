import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import datetime
from maka.models import *
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.http import JsonResponse
from apis.serializers import UserInteractionSerializer

"""
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.username = "Anonymous"
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.username)

    def receive(self, *, text_data):
        print('recieved')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print('Message:', message)

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))


    
    def disconnect(self, message):
        pass

"""

class LikesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'unread_messages'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        params = parse_qs(self.scope["query_string"].decode())
        print(params)
        user = params.get('user', (None,))[0]
        print(user)
        like_count = await self.get_like_count(user)
        print(like_count)
        await self.send(text_data=json.dumps({"unread_messages": like_count}))

    @database_sync_to_async
    def get_like_count(self, user_id):
        print("TEST TEST TEST TEST ")
        print(user_id)
        print(UserInteraction.objects.all().filter(target=user_id).count())
        return UserInteraction.objects.all().filter(target=user_id).count()

    @database_sync_to_async
    def update_seen_status(self, uid):
        print('Updating...')
        return UserInteraction.objects.all().filter(target=uid).update(seen=True)

    async def receive(self, text_data):
        req_body = json.loads(text_data)
        print(req_body['user_id'])
        await self.update_seen_status(uid=req_body['user_id'])
        #await self.send(text_data=json.dumps({"message": "Server confirmed status update"}))
        like_count = await self.get_like_count(req_body['user_id'])
        print(like_count)
        await self.send(text_data=json.dumps({"unread_messages": like_count}))

    async def disconnect(self, close_code):
        like_count = await self.get_like_count("ZnhatH8rseeZDoDBKSQJcnhprbl1")
        print(like_count)
        await self.send(text_data=json.dumps({"unread_messages": like_count}))
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    """async def connect(self):
        self.room_group_name = 'unread_messages'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        params = parse_qs(self.scope["query_string"].decode())
        user = params.get('user', (None,))[0]
        like_count = await self.get_like_count("ZnhatH8rseeZDoDBKSQJcnhprbl1")
        await self.send(text_data=json.dumps({"unread_messages": like_count}))

    @database_sync_to_async
    def get_like_count(self, user_id):
        return UserInteraction.objects.filter(
            target=user_id, seen=False, interaction_type='UserInteractionType.like'
        ).count()
        
    async def update_seen_status(self):
        await sync_to_async(UserInteraction.objects.all().update)(seen=True)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('Message:', message)
        # Query the database for new likes that the user has not seen yet
        unseen_likes = await sync_to_async(UserInteraction.objects.filter)(
            target="ZnhatH8rseeZDoDBKSQJcnhprbl1", seen=False, interaction_type='UserInteractionType.like'
        )
        for ui in unseen_likes:
            ui_json = UserInteractionSerializer(ui).data
        user_interaction = await sync_to_async(UserInteraction.objects.all)().iterator()

"""
    

class SecretMatchConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'secret'
        
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print('Message:', message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'time': datetime.datetime.now(),
                'message': message
            }
        )

    

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({'type':'chat',
        'time': str(datetime.datetime.now()),
        'message': message}))



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print('Message:', message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'time': datetime.datetime.now(),
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({'type':'chat',
        'time': str(datetime.datetime.now()),
        'message': message}))

