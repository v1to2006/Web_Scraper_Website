from django.urls import path
from .views import tractors

urlpatterns = [
    path('', tractors, name='tractors_view'),
]
