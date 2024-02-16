import mysql.connector, re, time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Database:
    def __init__(self, host, user, password, database_name):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database_name
        )

    def insert_game_into_database(self, game):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO webscrap.games_game (name, release_date, reviews_count, positive_reviews_percent, metacritic_score, price, img, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        query_values = (
            game.name,
            game.release_date,
            game.reviews_count,
            game.positive_reviews_percent,
            game.metacritic_score,
            game.price,
            game.img,
            game.url
        )
        cursor.execute(insert_query, query_values)
        self.connection.commit()

    def truncate_table(self):
        cursor = self.connection.cursor()
        truncate_query = "TRUNCATE TABLE webscrap.games_game"
        cursor.execute(truncate_query)
        self.connection.commit()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

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
            current_release_date = get_date_from_string(release_date.text)
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

def get_date_from_string(value):
    cleaned_value = value.strip()
    
    return datetime.strptime(cleaned_value, "%d %b, %Y")

def get_reviews_count(value):
    start_index = value.find("of the ") + len("of the ")
    end_index = value.find(" user reviews")
    reviews_count_str = value[start_index:end_index]
    
    return int(reviews_count_str.replace(',', ''))

def get_positive_reviews_percent(value):
    match = re.search(r'(\d+)%', value)
    
    return int(match.group(1))

game_list = find_games()

database = Database("localhost", "root", "", "webscrap")

database.truncate_table()

for game in game_list:
    database.insert_game_into_database(game)

print(f'Games scraped ({len(game_list)} found)')