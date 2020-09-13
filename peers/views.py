from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest

from typing import List, Dict
import base64
import hashlib, json
from peers.models import *
from peers.proto import PeerData_pb2 as pdpb
import time
import random
from channels_redis.core import RedisChannelLayer
from collections import defaultdict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.generic import View
from django.db.models import Model

from peers.exceptions import InvalidChannelError


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


MAX_RECURSION_DEPTH = 4
GAMES_MIN = 150


class DataLoader:
    """
    Loads Players from the DB and if they don't exist from the client.
    Peers always get loaded from the client
    """

    def __init__(self, channelId: str, layer: RedisChannelLayer):
        self._channelId = channelId
        self._layer = layer

    def getSinglePlayer(self, accountId: int) -> Player:
        """
        Wrapper for 'getPlayers' to fetch only one player
        :param accountId: Account id of the player to fetch
        :return: The Player object
        """

        return self.getPlayers([accountId])[0]

    def getSinglePeers(self, accountId: int) -> pdpb.PeersResponse:
        """
        Wrapper from 'getPeers' to fetch only one players peers
        :param accountId: Account id of the player to fetch the peers from
        :return: The PeersResponse object containing the peers
        """

        return self.getPeers([accountId])[0]

    def getPeers(self, accountIds: List[int]) -> List[pdpb.PeersResponse]:
        """
        Fetches the peers from the client
        :param accountIds: List of account ids to fetch the peers from
        :return: List of PeersResponse objects containing the peers data
        """

        req = pdpb.PeerDataRequest()

        # Populate request object
        for accountId in accountIds:
            req.peers.append(
                pdpb.PeersRequest(accountId=accountId)
            )

        resp = self._sendProto(req)

        return list(resp.peers)
    
    def getPlayers(self, accountIds: List[int]) -> List[Player]:
        """
        Loads a list of players based of their account ids from the DB or the client.
        :param accountIds: List of accountIds to load
        :return: List containing the loaded players
        """

        playerObjects = dict()
        req = pdpb.PeerDataRequest()

        # Get the already existing players
        for accountId in accountIds:
            playerObjects[accountId] = self._get_or_none(Player, accountId=accountId)

        # Create the request object of not found players
        for accountId, playerObj in playerObjects.items():
            if playerObj == None:
                req.players.append(
                    pdpb.PlayerRequest(accountId=accountId)
                )

        # Only send the request if players need to be requests
        if len(req.players) > 0:
            resp = self._sendProto(req)
            for player in resp.players:
                playerObjects[player.accountId] = self._createPlayerObj(player)

        return [playerObjects[id] for id in accountIds]
    
    def _sendProto(self, request: pdpb.PeerDataRequest) -> pdpb.PeerDataResponse:
        async_to_sync(self._layer.send)(self._channelId, {
            'type': 'proto_request',
            'data': base64.b64encode(request.SerializeToString()).decode()
        })

        try:
            resp_data = async_to_sync(self._layer.receive)(self._channelId + 'proto')
            resp = pdpb.PeerDataResponse()
            resp.ParseFromString(base64.b64decode(resp_data['data']))

            return resp

        # Raised then the channelId doesnt actually exist (anymore)
        except AssertionError as e:
            if str(e) != "Wrong client prefix":
                raise e
            con = Connections.objects.get(channel_id=self._channelId)
            con.delete()
            raise InvalidChannelError(con.channel_id, con.user_id) from None

    def _get_or_none(self, db_class: Model, **kwargs):
        """
        Returns an instance of a DB model if it exists. Otherwise returns None.
        :param db_class: DB class like Person or Peer
        :param kwargs: Kwargs to filter the DB.
        :return: The DB object or None
        """

        try:
            return db_class.objects.get(**kwargs)
        except db_class.DoesNotExist:
            return None

    def _createPlayerObj(self, playerResp: pdpb.PlayerResponse) -> Player:
        """
        Creates a Player object in the DB from a protobuf PlayerResponse.
        :return: The freshly created DB object
        """

        return Player.objects.create(
            accountId=playerResp.accountId,
            username=playerResp.username,
            rank=playerResp.rank,
            dotaPlus=playerResp.dotaPlus,
            steamId=playerResp.steamId,
            avatars=Avatars(
                small=playerResp.avatars.small,
                medium=playerResp.avatars.medium,
                large=playerResp.avatars.large,
            ),
            profileUrl=playerResp.profileUrl,
            countryCode=playerResp.countryCode,
            wins=playerResp.wins,
            loses=playerResp.loses,
            timestamp=datetime.datetime.now()
        )
        

class PeerLoader:
    """
    Loads the peers for a player.
    """

    def __init__(self, channelId: str, layer: RedisChannelLayer):
        self.channelId = channelId
        self.layer = layer
        self.username = None
        self.dataLoader = DataLoader(channelId, layer)
        self.accountId = None
        self._recursionDepthMap = dict()

    def load(self, accountId):
        self.accountId = accountId
        self._recursionDepthMap = dict()
        p = self.dataLoader.getSinglePlayer(accountId)

        self._load(p, recursionDepth=0, parent=None, plist=list())

    def _load(self, player: Player, recursionDepth=0, parent=None, plist=None):
        """
        Recursive method to load the peers and the associated players for a player.
        """

        # Exit if the max recursion depth is reached
        if recursionDepth > MAX_RECURSION_DEPTH:
            return

        # Only continue loading when the player gets loaded earlier in the recursion so more of the players peers can be loaded
        if self._recursionDepthMap.get(player.accountId, 1000) <= recursionDepth:
            return
        self._recursionDepthMap[player.accountId] = recursionDepth

        print(player.username + ": " + ' -> '.join([p.username for p in plist]))

        peers = self.dataLoader.getSinglePeers(player.accountId).peers
        relevantPeers = [p for p in peers if p.games >= GAMES_MIN]

        # Pre-Load the players required for the peers
        targetList = self.dataLoader.getPlayers([p.accountId2 for p in relevantPeers])

        assert len(relevantPeers) == len(targetList)    # Make sure the data is correct

        for peer, target in zip(peers, targetList):
            # Dont loop back to the parent
            if parent != None and target == parent:
                continue

            # Dont start a loop from earlier
            if target in plist:
                continue

            peers1 = Peer.objects.filter(player=player, player2=target).all()
            if not peers1:
                self._addPeers(player, target, peer.wins, peer.games)

            self._load(target, recursionDepth=recursionDepth + 1, parent=player, plist=plist + [player])

        player._peersLoaded = True
        player.save()

    def _addPeers(self, player, target, games, wins):
        """
        Adds the peers data for two players
        """

        peer1 = Peer(player=player, player2=target)
        peer2 = Peer(player=target, player2=player)
        data = PeerData(games=games, wins=wins)
        peer1.data = data
        peer2.data = data

        data.save()
        peer1.save()
        peer2.save()


class GenerateView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layer = get_channel_layer()
        self.request = None
        self.id = None

    @property
    def layer(self) -> RedisChannelLayer:
        return self._layer

    def createId(self):
        """
        Creates a unique connection ID
        """

        metaValue = json.dumps(self.request.META).encode()
        timeValue = str(time.time()).encode()
        randValue = random.randbytes(100)

        return hashlib.md5(metaValue + timeValue + randValue).hexdigest()

    def getChannelId(self):
        connections = Connections.objects.filter(user_id='id_' + str(self.id))
        if len(connections) == 0:
            return -1
        elif len(connections) > 1:
            return 2
        return connections.first().channel_id

    def get(self, request: WSGIRequest, id: int):
        self.request = request
        self.id = id

        channelId = self.getChannelId()
        if channelId == -1:
            return HttpResponse("No agent connected.")
        elif channelId == -2:
            return HttpResponse("Multiple agents connected")

        pl = PeerLoader(self.getChannelId(), self.layer)
        pl.load(PLAYER_ID)


        return HttpResponse("Done")

    def _sendRequest(self, request: pdpb.PeerDataRequest) -> pdpb.PeerDataResponse:
        connections = Connections.objects.filter(user_id='id_' + str(self.id))
        if len(connections) == 0:
            return -1
        elif len(connections) > 1:
            return 2
        con = connections.first()

        async_to_sync(self.layer.send)(con.channel_id, {
            'type': 'proto_request',
            'data': base64.b64encode(request.SerializeToString()).decode()
        })

        resp_data = async_to_sync(self.layer.receive)(con.channel_id + 'proto')
        resp = pdpb.PeerDataResponse()
        resp.ParseFromString(base64.b64decode(resp_data['data']))

        return resp

