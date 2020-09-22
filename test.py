import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
import django
django.setup()

from peers.models import *

p1 = Player.objects.get(username='Archangel Azrael')
p2 = Player.objects.get(username='baschi29')

Player.objects.all().delete()

pass