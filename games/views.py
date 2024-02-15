from django.shortcuts import render
from .models import Game

def game_list(request):
    games = Game.objects.all().order_by('release_date').reverse()
    return render(request, 'games/games.html', {'games': games})
