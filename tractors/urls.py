from django.urls import path
from .views import tractor_list

urlpatterns = [
    path('', tractor_list, name='tractors_view'),
]
