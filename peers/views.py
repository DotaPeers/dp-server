from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest

from pathlib import Path
from typing import List, Dict
import base64
import hashlib, json
from peers.models import *
from peers.proto import PeerData_pb2 as pdpb
import time
from channels_redis.core import RedisChannelLayer
from collections import defaultdict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.generic import View
from django.db.models import Model

from peers.exceptions import InvalidChannelError, ConnectionError
from peers.utility import getProfilePicturePath


PLAYER_ID = 154605920
MAX_RECURSION_DEPTH = 4
GAMES_MIN = 150
DATA_LIFETIME = 30   # in days


""" ToDo:
    + Only load data from the client that is not in the DB
    + Reload data if it is expired
    - Nicer looking GUI
    - Basic website
    + ProtoClient more exception proof
"""


def createId(request: WSGIRequest):
    """
    Creates a unique connection ID
    """
    metaValue = json.dumps(request.META).encode()
    timeValue = str(time.time()).encode()
    randValue = os.urandom(100)

    return hashlib.md5(metaValue + timeValue + randValue).hexdigest()


class ClientManager:
    """
    Interaction with the client and the database.

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
            playerObjects[accountId] = self._get_player_if_valid(accountId)

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

    def sendMetadata(self, start=False, end=False) -> None:
        assert not (start == True and end == True)

        req = pdpb.PeerDataRequest()
        if start:
            req.metadata.start = start
        if end:
            req.metadata.end = end

        resp = self._sendProto(req)

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

    def _get_player_if_valid(self, accountId):
        """
        Tries to fetch a Player object from the database. The player objects gets deleted, if it's too old.
        :return: Player object or None
        """

        player = self._get_or_none(Player, accountId=accountId)  # type: Player
        if player:
            if datetime.datetime.now() - player.timestamp > datetime.timedelta(days=DATA_LIFETIME):
                player.delete()
                return None

        return player

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

    def _savePlayerProfilePicture(self, playerResp: pdpb.PlayerResponse) -> None:
        """
        Tries to save the profile picture data to the images folder
        """

        with open(Config.PROFILE_PICTURES_FOLDER + '/' + getProfilePicturePath(playerResp.accountId), 'wb') as file:
            file.write(playerResp.profilePicture)

    def _createPlayerObj(self, playerResp: pdpb.PlayerResponse) -> Player:
        """
        Creates a Player object in the DB from a protobuf PlayerResponse.
        :return: The freshly created DB object
        """

        # Save the profile picture
        try:
            self._savePlayerProfilePicture(playerResp)
        except FileNotFoundError:
            Path(getProfilePicturePath(playerResp.accountId)).mkdir(parents=True, exist_ok=True)
            self._savePlayerProfilePicture(playerResp)

        # Create the player
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

    def __init__(self, clientManager: ClientManager):
        self.clientManager = clientManager
        self.username = None
        self.accountId = None
        self._recursionDepthMap = dict()

    def load(self, accountId):
        self.clientManager.sendMetadata(start=True)
        self.accountId = accountId
        self._recursionDepthMap = dict()
        p = self.clientManager.getSinglePlayer(accountId)

        self._load(p, recursionDepth=0, parent=None, plist=list())

        self.clientManager.sendMetadata(end=True)

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

        # Only load peers if they were not fully loaded
        if player.peersLoaded:
            return

        # print(player.username + ": " + ' -> '.join([p.username for p in plist]))

        peers = self.clientManager.getSinglePeers(player.accountId).peers
        relevantPeers = [p for p in peers if p.games >= GAMES_MIN]

        # Pre-Load the players required for the peers
        targetList = self.clientManager.getPlayers([p.accountId2 for p in relevantPeers])

        assert len(relevantPeers) == len(targetList)  # Make sure the data is correct

        for peer, target in zip(peers, targetList):
            # Dont loop back to the parent
            if parent != None and target == parent:
                continue

            # Dont loop back to an earlier player in the chain
            if target in plist:
                continue

            peers = Peer.objects.filter(player=player, player2=target).first()
            if peers:
                # Delete the peers if they are outdated
                if datetime.datetime.now() - peers.data.timestamp > datetime.timedelta(days=DATA_LIFETIME):
                    peers.data.delete()
                    self._addPeers(player, target, peer.wins, peer.games)

            else:
                self._addPeers(player, target, peer.wins, peer.games)

            self._load(target, recursionDepth=recursionDepth + 1, parent=player, plist=plist + [player])

        player.peersLoaded = True
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


def index(request: WSGIRequest):

    return render(request, 'index.haml')


def test(request: WSGIRequest):

    def getChannelId():
        connections = Connections.objects.filter(user_id='id_12345')
        if len(connections) == 0:
            return -1
        elif len(connections) > 1:
            return 2
        return connections.first().channel_id

    Player.objects.all().delete()

    pl = PeerLoader(getChannelId(), get_channel_layer())
    pl.load(PLAYER_ID)

    return HttpResponse('Testing...')


class InformationView(View):

    def get(self, request: WSGIRequest):
        return render(request, 'information.haml')


class AboutView(View):

    def get(self, request: WSGIRequest):
        return render(request, 'about.haml')


class GetIdView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = None     # type: WSGIRequest

    def get(self, request: WSGIRequest):
        self.request = request

        context = {
            'id_active': True,
        }

        return render(request, 'get_id.haml', context)

    def post(self, request: WSGIRequest):
        self.request = request

        post = dict(request.POST)

        if 'requestId' in post:
            if 'new' in post['requestId']:
                return self.requestId(new=True)
            return self.requestId()

        if 'agentConnected' in post:
            return self.checkAgentConnected()

        raise RuntimeError(f"Unknown POST data {post}.")

    def requestId(self, new=False):
        """
        Generates the ID for the user
        :param new: If True requests a new ID, even if one exists already
        :return: The ID
        """

        if not new:
            if 'userId' in self.request.session:
                return HttpResponse(json.dumps({'id': self.request.session['userId'], 'status': 'SESSION'}))

        userId = createId(self.request)
        self.request.session['userId'] = userId

        return HttpResponse(json.dumps({'id': userId, 'status': 'NEW'}))

    def checkAgentConnected(self):
        response = {
            'connected': False
        }

        userId = self.request.session['userId'] if 'userId' in self.request.session else None

        if userId:
            conn = Connections.objects.filter(user_id=f'id_{userId}')
            if conn:
                response['connected'] = True

        return HttpResponse(json.dumps(response))


class GenerateView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = None  # type: WSGIRequest

    def get(self, request: WSGIRequest):
        self.request = request

        context = {
            'id_active': True,
        }

        return render(request, 'generate.haml', context)

    def post(self, request: WSGIRequest):

        post = dict(request.POST)

        if 'playerId' in post:
            return self.onPlayerIdFormSubmit(int(post.get('playerId')[0]))

        if 'startGenerationFor' in post:
            return self.downloadDataFor(int(post.get('startGenerationFor')[0]))

        raise RuntimeError(f"Unknown POST data {post}.")

    def _getClientManager(self):
        connections = Connections.objects.filter(user_id='id_' + str(self.request.session['userId']))
        if len(connections) == 0:
            raise ConnectionError("No connection found.", 1)
        elif len(connections) > 1:
            raise ConnectionError("Multiple connections found.", 2)
        channelId = connections.first().channel_id

        return ClientManager(channelId, get_channel_layer())

    def onPlayerIdFormSubmit(self, playerId):
        clientManager = self._getClientManager()

        if not playerId or playerId == '':
            return HttpResponse("The player ID can't be empty.", status=555)

        player = clientManager.getSinglePlayer(playerId)

        context = {
            'picturePath': f'/static/{getProfilePicturePath(playerId)}',
            'accountId': player.accountId,
            'username': player.username,
            'steamId': player.steamId,
            'countryCode': player.countryCode,
            'games': player.games,
            'wins': player.wins,
            'loses': player.loses,
            'dotaPlus': player.dotaPlus,
            'rankPath': f'/static/img/medals/medal-{player.rank.convertBack()}.webp',
        }

        return HttpResponse(json.dumps(context))

    def downloadDataFor(self, playerId: int):

        pl = PeerLoader(self._getClientManager())
        pl.load(PLAYER_ID)

        return HttpResponse(json.dumps({"status": "Done"}))


class GenView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._layer = get_channel_layer()
        self.request = None
        self.id = None

    @property
    def layer(self) -> RedisChannelLayer:
        return self._layer

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
        status = 0
        if channelId == -1:
            status = -1
        elif channelId == -2:
            status = -2


        if status == 0:
            pl = PeerLoader(self.getChannelId(), self.layer)
            pl.load(PLAYER_ID)

        context = {
            "status": status
        }

        return render(request, 'gen.haml', context)
