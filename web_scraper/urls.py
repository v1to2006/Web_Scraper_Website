from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cars/', include('cars.urls')),
    path('tractors/', include('tractors.urls')),
    path('games/', include('games.urls')),
]
