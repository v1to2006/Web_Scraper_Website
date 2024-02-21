import json
from django.shortcuts import render
from django.http import HttpResponseServerError

def games(request):
    file_path = 'C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/games_results.json'

    try:
        with open(file_path, 'r') as file:
            games = json.load(file)
    except FileNotFoundError:
        return HttpResponseServerError("Tractors data file not found.")
    except json.JSONDecodeError:
        return HttpResponseServerError("Error decoding JSON data.")

    return render(request, 'games/games.html', {'games': games})
