import json
from django.shortcuts import render
from django.http import HttpResponseServerError

def cars(request):
    file_path = 'C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/cars_results.json'

    try:
        with open(file_path, 'r') as file:
            cars = json.load(file)
    except FileNotFoundError:
        return HttpResponseServerError("Tractors data file not found.")
    except json.JSONDecodeError:
        return HttpResponseServerError("Error decoding JSON data.")

    return render(request, 'cars/cars.html', {'cars': cars})
