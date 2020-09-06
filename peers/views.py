from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest

import base64
from peers.models import *
from peers.proto import PeerData_pb2 as pdpb
from PeerLoader import PeerLoader
import time
from channels_redis.core import RedisChannelLayer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.generic import View


PLAYER_ID = 154605920


def index(request: WSGIRequest):

    return HttpResponse('Index')


def test(request: WSGIRequest):

    layer = get_channel_layer()

    async_to_sync(layer.group_send)('id_12345', {
        'type': 'chat_message',
        'message': 'Hello from View'
    })

    return HttpResponse('Testing...')



class GenerateView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._layer = get_channel_layer()
        self.id = None

    @property
    def layer(self) -> RedisChannelLayer:
        return self._layer


    def get(self, request: WSGIRequest, id: int):
        self.id = id

        req = pdpb.PeerDataRequest()
        req.players.append(
            pdpb.PlayerRequest(accountId=PLAYER_ID)
        )

        resp = self._sendRequest(req)

        return HttpResponse(str(resp))


    def _sendRequest(self, request: pdpb.PeerDataRequest) -> pdpb.PeerDataResponse:
        con = Connections.objects.get(user_id='id_' + str(self.id))

        async_to_sync(self.layer.send)(con.channel_id, {
            'type': 'proto_request',
            'data': base64.b64encode(request.SerializeToString()).decode()
        })

        resp_data = async_to_sync(self.layer.receive)(con.channel_id + 'proto')
        resp = pdpb.PeerDataResponse()
        resp.ParseFromString(base64.b64decode(resp_data['data']))

        return resp

