import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from channels_redis.core import RedisChannelLayer

from peers.models import *


class ProtobufConsumer(AsyncWebsocketConsumer):

    @property
    def layer(self) -> RedisChannelLayer:
        return self.channel_layer

    @database_sync_to_async
    def _get_connection(self, user_id):
        try:
            return Connections.objects.filter(user_id=user_id).first()
        except Connections.DoesNotExist:
            return None

    @database_sync_to_async
    def _delete_connection(self, user_id):
        old = Connections.objects.filter(user_id=user_id).first()
        if old:
            old.delete()

    @database_sync_to_async
    def _add_connection(self, user_id, channel_id):
        return Connections.objects.create(user_id=user_id, channel_id=channel_id)


    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.id_name = 'id_%s' % self.id

        # Delete existing connections if they exist. (Remove later)
        await self._delete_connection(self.id_name)

        # A client is already connected
        # if await self._get_connection(self.id_name):
        #     await self.disconnect(1001)
        #     return

        await self._add_connection(self.id_name, self.channel_name)
        await self.accept()


    async def disconnect(self, code):
        print('Disconnected with code {}.'.format(code))
        await self._delete_connection(self.id_name)


    async def receive(self, text_data=None, binary_data=None):
        # print('Received {} and {}.'.format(text_data, binary_data))
        text_data_json = json.loads(text_data)

        if text_data_json['type'] != 'proto_response':
            raise RuntimeError('Message type cant be {}.'.format(text_data_json['type']))

        await self.layer.send(self.channel_name + 'proto', {
            'type': 'proto_response',
            'data': text_data_json['data']
        })


    async def proto_request(self, event):
        # print("Proto request: " + str(event))
        await self.send(event['data'])

    async def proto_response(self, event):
        print('Proto response: ' + str(event))
        raise RuntimeError('Response at wrong location')


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.id_name = 'id_%s' % self.id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.id_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.id_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.id_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message + " jo jo jo !!!"
        }))


# class ProtobufConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.id = self.scope['url_route']['kwargs']['id']
#         self.id_name = 'id_%s' % self.id
#
#         # Delete existing connections if they exist. (Remove later)
#         old = Connections.objects.filter(user_id=self.id_name).first()
#         if old:
#             old.delete()
#
#         Connections.objects.create(user_id=self.id_name, channel_id=self.channel_name)
#
#         self.accept()
#
#     def disconnect(self, code):
#         print('Disconnected with code {}.'.format(code))
#         Connections.objects.get(user_id=self.id_name).delete()
#
#     def receive(self, text_data=None, binary_data=None):
#         print('Received {} and {}.'.format(text_data, binary_data))
#
#         async_to_sync(self.channel_layer.send)(self.channel_name, {
#             'type': text_data['type'],
#             'data': text_data['data']
#         })
#
#     def proto_request(self, event):
#         print("Proto request: " + str(event))
#         self.send(event['data'])
#
#     def proto_response(self, event):
#         print('Proto response ' + str(event))
#         self.send(event['data'])
