import time, os

def run_scraper(scraper):
    command = f'py C:\GitHub\Web\Web_Scraper_Project\Web_Scraper_Website\scrapers\{scraper}'
    os.system(command)

scrapers = ['cars_scraper.py', 'tractors_scraper.py', 'games_scraper.py']

while True:
    for scraper in scrapers:
        run_scraper(scraper)
    
    time.sleep(3600)
