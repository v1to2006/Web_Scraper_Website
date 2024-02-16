from django.contrib import admin
from cars.models import Car
from tractors.models import Tractor
from games.models import Game

admin.site.register(Car)
admin.site.register(Tractor)
admin.site.register(Game)

