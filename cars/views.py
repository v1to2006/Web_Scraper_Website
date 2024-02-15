from django.shortcuts import render
from .models import Car

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/cars.html', {'cars': cars})