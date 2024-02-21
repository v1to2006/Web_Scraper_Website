import re, time, json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class Game:
    def __init__(self, name, release_date, reviews_count, positive_reviews_percent, metacritic_score, price, img, url):
        self.name = name
        self.release_date = release_date
        self.reviews_count = reviews_count
        self.positive_reviews_percent = positive_reviews_percent
        self.metacritic_score = metacritic_score
        self.price = price
        self.img = img
        self.url = url

def find_games():
    games = []
    main_url = 'https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&os=win&supportedlang=english%2Crussian%2Cfinnish&filter=popularnew&ndl=1'

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:
        driver.get(main_url)
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        name_elements = soup.find_all("span", class_="title")
        release_dates = soup.find_all("div", class_="col search_released responsive_secondrow")
        game_elements = soup.find_all("span", class_="search_review_summary positive")
        prices = soup.find_all("div", class_="col search_discount_and_price responsive_secondrow")
        images = soup.find_all("div", class_="col search_capsule")
        urls = soup.find_all('a', {'data-ds-appid': True})

        for name_element, release_date, game_element, price, image, url in zip(name_elements, release_dates, game_elements, prices, images, urls):
            current_name = name_element.text
            current_release_date = release_date.text
            current_reviews_count = get_reviews_count(game_element["data-tooltip-html"])
            current_positive_reviews_percent = get_positive_reviews_percent(game_element["data-tooltip-html"])

            price_element = price.find("div", class_=["discount_final_price", "discount_final_price free"])

            if price_element and price_element.text == "Free":
                current_price = 0.0
            elif price_element:
                current_price = float(price_element.text.replace('\u20ac', '').replace(',', '.'))
            else:
                current_price = 0.0

            current_image = image.find("img")["src"]
            current_url = url.get("href")

            current_metacritic_score = get_metacritic_score(current_url, driver)

            games.append(Game(current_name, current_release_date, current_reviews_count, current_positive_reviews_percent,
                              current_metacritic_score, current_price, current_image, current_url))

    return games


def get_metacritic_score(game_url, driver):
    driver.get(game_url)
    time.sleep(0.1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    metacritic_score_div = soup.find('div', {'id': "game_area_metascore"})

    if metacritic_score_div:
        metacritic_score = metacritic_score_div.find('div', class_="score high")

        if metacritic_score:
            return int(metacritic_score.text.strip())

    return 0

def get_reviews_count(value):
    start_index = value.find("of the ") + len("of the ")
    end_index = value.find(" user reviews")
    reviews_count_str = value[start_index:end_index]
    
    return int(reviews_count_str.replace(',', ''))

def get_positive_reviews_percent(value):
    match = re.search(r'(\d+)%', value)
    
    return int(match.group(1))

def save_to_json(filename):
    with open(filename, 'w') as json_file:
        game_list_data = [vars(game) for game in game_list]
        json.dump(game_list_data, json_file, indent=2)
       
        print(f"Games results saved to {filename}")

game_list = find_games()

save_to_json("C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/games_results.json")

print(f'Games scraped ({len(game_list)} found)')