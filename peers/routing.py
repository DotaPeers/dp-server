from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/proto/<str:id>', consumers.ProtobufConsumer),
]
