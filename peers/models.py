import os
import datetime
from PIL import Image, ImageDraw, ImageOps
import io
import django
from django.db import models
from django.db.models.query import Q

import Config
from peers.data.Rank import Rank
from peers.utility import getProfilePicturePath


# -----  Custom types  -----

class RankType(models.IntegerField):
    """
    Represents a Rank in Dota 2
    """

    description = "A Dota 2 rank like Legend 1, or Uncalibrated"

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value

        elif isinstance(value, Rank):
            return str(value. convertBack())

        elif isinstance(value, int):
            return str(value)

        raise RuntimeError("Value for RankType can't be '{}'. Must be Rank, int or None.".format(value))

    def to_python(self, value):
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Rank(value)

# -----  Models  -----

class Avatars(models.Model):

    small  = models.TextField(max_length=255)
    medium = models.TextField(max_length=255)
    large  = models.TextField(max_length=255)

    def __str__(self) -> str:
        return 'Avatars<>'


class Player(models.Model):

    accountId = models.IntegerField(primary_key=True)
    username = models.TextField(null=False)
    rank = RankType(null=True)
    dotaPlus = models.BooleanField(null=True)
    steamId = models.TextField(null=True, max_length=255)
    avatars = models.OneToOneField(Avatars, null=True, on_delete=models.CASCADE)
    profileUrl = models.TextField(null=True, max_length=255)
    countryCode = models.TextField(null=True, max_length=8)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)

    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    _peersLoaded = models.BooleanField(default=False)   # Determines if all of its peers were loaded

    def save(self, **kwargs):
        """
        Save the avatars object first, then save this object
        """

        if self.avatars:
            self.avatars.save()
        super().save(**kwargs)

    def _post_delete_handler(self):
        """
        This method gets called everytime after a Player object was deleted. This gets used to delete the avatar objects
        and the profile pictures.
        Without this hack the PeerData objects wouldn't get deleted
        """

        self._additional_delete()

    def _additional_delete(self):
        """
        Delete children that wouldn't get deleted otherwise
        """

        # Delete the Avatars
        try:
            self.avatars.delete()
        except Avatars.DoesNotExist:
            pass
        except AssertionError:
            pass

        # Delete the profile pictures
        path = getProfilePicturePath(self.accountId) + f'/{self.accountId}.png'
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


    @property
    def peers(self):
        return self._from_peers_set.all()

    @property
    def games(self):
        return self.wins + self.loses

    @property
    def winrate(self):
        return round(100 / (self.wins + self.loses) * self.wins, 2)

    def __str__(self) -> str:
        return 'Player<id={}, username={}>'.format(self.accountId, self.username)


class Peer(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='_from_peers_set')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='_to_peers_set')
    data = models.ForeignKey('PeerData', on_delete=models.CASCADE, null=False)

    def _post_delete_handler(self):
        """
        This method gets called everytime after a Peer object was deleted. This gets used to delete the data objects.
        Without this hack the PeerData objects wouldn't get deleted
        """

        self._additional_delete()

    def _additional_delete(self):
        """
        Deletes children that wouldn't get deleted otherwise
        """

        # Delete the data object, which will in turn also delete the other peer object
        try:
            self.data.delete()
        except PeerData.DoesNotExist:
            pass
        except AssertionError:
            pass


    def __str__(self):
        return f'Peer<{self.player.username} -> {self.player2.username}>'


class PeerData(models.Model):

    games = models.IntegerField(null=False)
    wins = models.IntegerField(null=False)

    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    @property
    def loses(self):
        return self.games - self.wins

    @property
    def winrate(self):
        return round(100 / self.games * self.wins, 2)

    def __str__(self):
        return 'PeerData<>'


class Connections(models.Model):

    user_id = models.TextField(unique=True)
    channel_id = models.TextField()

    def __repr__(self):
        return 'Connection<{}>'.format(self.user_id)

# -----  Django Signals  -----

def post_delete_handler(sender, instance, **kwargs):
    """
    Dispatches all post_delete signals
    """

    if isinstance(instance, Peer):
        instance._post_delete_handler()
    elif isinstance(instance, Player):
        instance._post_delete_handler()


models.signals.post_delete.connect(post_delete_handler)
