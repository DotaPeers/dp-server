from peers.models import *


def onStartup():
    """
    Executed once on startup
    """

    Connections.objects.all().delete()
