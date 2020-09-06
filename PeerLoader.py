

MAX_RECURSION_DEPTH = 3


class PeerLoader(object):

    def __init__(self, player):
        self.player = player
        self._recursionDepthMap = dict()

    def load(self):
        self._load(self.player, plist=[self.player])

    def _load(self, player, recursionDepth=0, parent=None, plist=[]):
        if recursionDepth > MAX_RECURSION_DEPTH:
            return

        # Only continue loading when the player gets loaded earlier in the recursion so more of the players peers can be loaded
        if player.accountId in self._recursionDepthMap and self._recursionDepthMap[player.accountId] >= recursionDepth:
            return
        self._recursionDepthMap[player.accountId] = recursionDepth

        print(player.username + ": " + ' -> '.join([p.username for p in plist]))


        data = self._loadData('players/{}/peers'.format(player.accountId))
        relevant = [p for p in data if p['with_games'] >= Config.GAMES_PLAYED_MIN]

        for p in relevant:
            target = self._get_player(p['account_id'])

            # Dont go back to the parent
            if target == parent:
                continue

            # Dont loop around
            if target in plist:
                continue
            peers1 = Peer.objects.filter(player1=target, player2=player).all()
            peers2 = Peer.objects.filter(player1=player, player2=target).all()
            # peers1 = self.session.query(Peer).filter_by(player1=target, player2=player).all()
            # peers2 = self.session.query(Peer).filter_by(player1=player, player2=target).all()
            if not peers1 and not peers2:
                self._add_peer(player, target, p['with_games'], p['with_win'])

            self._load(target, recursionDepth=recursionDepth + 1, parent=player, plist=plist + [target])


    def _add_peer(self, player, target, games, wins):
        """
        Adds a peer from player to target
        """

        peer = Peer(player1=player, player2=target, games=games, wins=wins, timestamp=datetime.datetime.now())
        peer.save()


    def _get_player(self, account_id):
        """
        Gets a player object from the DB if it exists. If not loads it from the db and saves it there.
        """

        try:
            player = Player.objects.get(accountId=account_id)
        except models.ObjectDoesNotExist:
            player = Player(accountId=account_id)
            player.load()

        return player

