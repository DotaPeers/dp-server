import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
import django
django.setup()

from peers.models import *

import networkx as nx
from fa2 import ForceAtlas2
from fa2l import force_atlas2_layout
import math
import time

import pyvis
from pyvis.network import Network
from pyvis import options


PLAYER_ID = 154605920


class GraphGenerator:

    def __init__(self, player):
        self.player = player

    def __linearGamesToSize(self, games: int):
        size = games / 100

        if size < 20:
            return 10

        elif size > 100:
            return 50

        return size

    def __sigmoidGamesToSize(self, games: int):
        streckungY = 28
        streckungX = 40
        rechtsShift = 1.2
        upshift = 5
        gamesDivisor = 100

        return streckungY * math.tanh((games / gamesDivisor / streckungX) - rechtsShift) + streckungY + upshift

    def _gamesToNodeSize(self, games: int):
        return self.__sigmoidGamesToSize(games)

    def _gamesToEdgeWeight(self, games: int):
        """
        The weight of an edge
        """

        return games / 0.1

    def _gamesToEdgeValue(self, games: int):
        """
        The thickness of the edge line
        """

        return games / 10

    def _addNode(self, G: nx.Graph, player: Player):
        G.add_node(player.username,
                   size=self._gamesToNodeSize(player.games),
                   shape='image',
                   image=player.profilePicturePath,
                   title="Username: {} <br> County: {} <br>Games: {} <br>Wins: {} <br>Loses: {} <br>Winrate: {} <br>Rank: {}"
                   .format(player.username, player.countryCode, player.games, player.wins, player.loses, player.winrate,
                           player.rank.toStr()),
                   )

    def _addEdge(self, G: nx.Graph, player: Player, peer: Peer):
        player1 = player
        player2 = peer.player2
        data = peer.data

        G.add_edge(player1.username, player2.username,
                   weight=self._gamesToEdgeWeight(data.games),
                   value=self._gamesToEdgeValue(data.games),
                   title='{} -> {} <br>Games: {} <br>Wins: {} <br>Loses: {} <br>Winrate: {}'
                   .format(player1.username, player2.username, data.games, data.wins, data.loses, data.winrate),
                   )

    def _getEdges(self, G: nx.Graph, player: Player, depth=0, parent: Player = None):

        if player.username not in G.nodes:
            self._addNode(G, player)

        for p in player.peers:
            p1 = p.player.username
            p2 = p.player2.username

            if p.player2.username not in G.nodes:
                self._addNode(G, p.player2)

            if not G.has_edge(p1, p2) and not G.has_edge(p2, p1):
                self._addEdge(G, player, p)

            if depth < Config.MAX_RECURSION_DEPTH:
                self._getEdges(G, p.player2, depth=depth + 1, parent=player)

    def _getOptions(self):
        opt = options.Options()

        return opt

    def _getGraphData(self):
        G = nx.Graph()

        self._getEdges(G, self.player, depth=0, parent=None)

        return G

    def _forceAtlas2Layout_1(self, G: nx.Graph, iterations: int):
        """
        Uses this implementation: https://github.com/bhargavchippada/forceatlas2
        """

        forceatlas2 = ForceAtlas2(
            outboundAttractionDistribution=True,
            # Distributes attraction along outbound edges. Hubs attract less and thus are pushed to the borders
            edgeWeightInfluence=0,
            # How much influence you give to the edges weight. 0 is "no influence" and 1 is "normal"

            # Performance
            jitterTolerance=0.8,
            # How much swinging you allow. Above 1 discouraged. Lower gives less speed and more precision
            barnesHutOptimize=True,  # Barnes Hut optimization, n2 complexity to n.ln(n)
            barnesHutTheta=1,

            # Tuning
            scalingRatio=0.6,  # How much repulsion you want. More makes a more sparse graph (spärlich)
            strongGravityMode=False,  # A stronger gravity view
            gravity=1.0,  # Attracts nodes to the center. Prevents islands from drifting away

            # Log
            verbose=True
        )

        return forceatlas2.forceatlas2_networkx_layout(G, iterations=iterations)

    def _forceAtlas2Layout_2(self, G: nx.Graph, iterations: int):
        """
        Uses this implementation: https://pypi.org/project/fa2l/
        """

        t_start = time.time()
        pos = force_atlas2_layout(G, iterations=iterations,
                                  pos_list=None,
                                  node_masses=None,
                                  # Hubs attract less and are pushed to the borders
                                  outbound_attraction_distribution=False,
                                  # Makes clusters more tight
                                  lin_log_mode=False,
                                  # Prevent overlaping
                                  prevent_overlapping=True,
                                  edge_weight_influence=1.0,

                                  # Lower gives less speed and more precision
                                  jitter_tolerance=0.2,
                                  # Allows larger graphs
                                  barnes_hut_optimize=True,
                                  barnes_hut_theta=0.5,

                                  # Amount of repulsion
                                  scaling_ratio=0.2,
                                  strong_gravity_mode=False,
                                  # Attracts nodes to the center
                                  gravity=0.5
                                  )
        duration = time.time() - t_start
        print('Generation with {} iterations took {} seconds.'.format(iterations, round(duration, 2)))

        return pos


    def generateNetwork(self):
        G = self._getGraphData()

        # Generate the positions of the nodes
        pos = self._forceAtlas2Layout_1(G, 10000)
        # pos = self._forceAtlas2Layout_2(G, 1000)

        # Add the generated positions to the nodes
        for node in G.nodes:
            G.nodes[node]['pos'] = list(pos[node])

        return G, pos

    def generateGraph(self):
        G, pos = self.generateNetwork()

        nt = Network(height='90%', width='100%', heading=f"Dota Peers for {self.player.username}")
        nt.toggle_physics(False)
        nt.from_nx(G)

        nt.save_graph(f'{Config.GRAPH_PATHS}/{self.player.accountId}.html')


if __name__ == '__main__':
    player = Player.objects.get(accountId=PLAYER_ID)
    gen = GraphGenerator(player)
    gen.generateGraph()
