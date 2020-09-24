import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
import django
django.setup()

from peers.models import *

Player.objects.all().delete()

pass