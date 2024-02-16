from django.shortcuts import render
from .models import Tractor

def tractor_list(request):
    tractors = Tractor.objects.all()
    return render(request, 'tractors/tractors.html', {'tractors': tractors})
