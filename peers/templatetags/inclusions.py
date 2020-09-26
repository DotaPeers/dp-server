from django import template
from peers.models import Player

register = template.Library()


class PlayerInfoData:

    def __init__(self, playerId):
        self._playerId = playerId
        self._player = None     # type: Player
        if playerId:
            self._player = Player.objects.get(accountId=playerId)

    @property
    def status(self):
        if self._player:
            return 'OK'

        return 'PLAYER_NOT_SET'

    @property
    def picturePath(self):
        if self._player:
            return self._player.profilePicturePath

        return '/static/img/default-profile-picture.png'

    @property
    def accountId(self):
        if self._player:
            return self._player.accountId

        return '---'

    @property
    def username(self):
        if self._player:
            return self._player.username

        return '---'

    @property
    def steamId(self):
        if self._player:
            return self._player.steamId

        return '---'

    @property
    def countryCode(self):
        if self._player:
            return self._player.countryCode

        return '---'

    @property
    def games(self):
        if self._player:
            return self._player.games

        return '---'

    @property
    def wins(self):
        if self._player:
            return self._player.wins

        return '---'

    @property
    def loses(self):
        if self._player:
            return self._player.loses

        return '---'

    @property
    def dotaPlus(self):
        if self._player:
            if self._player.dotaPlus:
                return 'Yes'
            return 'No'

        return '---'

    @property
    def rankPath(self):
        if self._player:
            return f'/static/img/medals/medal-{self._player.rank.convertBack()}.webp'

        return '/static/img/medals/medal-0.webp'


    def toDict(self) -> dict:
        return {
            'status': self.status,
            'picturePath': self.picturePath,
            'accountId': self.accountId,
            'username': self.username,
            'steamId': self.steamId,
            'countryCode': self.countryCode,
            'games': self.games,
            'wins': self.wins,
            'loses': self.loses,
            'dotaPlus': self.dotaPlus,
            'rankPath': self.rankPath,
        }

    def __str__(self):
        return f'PlayerInfoData<{self._playerId}>'


@register.inclusion_tag('snippets/player_info.haml', takes_context=True)
def include_playerinfo(context):
    """
    This tag includes the player_info snippet. To work correctly, this tag needs the context to contain the key
    'playerInfoId' with a valid Player Id or None.
    :param context: Context object containing the request object and other parameters
    """

    viewContext = context.dicts[3]
    playerId = viewContext.get('playerInfoId', None)

    return {'playerData': PlayerInfoData(playerId=playerId)}
