from django.urls import path
from .views import game_list

urlpatterns = [
    path('', game_list, name='games_view'),
]
