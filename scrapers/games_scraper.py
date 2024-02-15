import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector

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
        self.truncate_table()

    def insert_into_database(self, url, theme, header, time_created, image_url):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO yle.kymenlaakso_articles (article_url, article_theme, article_header, article_time_created, article_image_url) VALUES (%s, %s, %s, %s, %s)"
        query_values = (url, theme, header, time_created, image_url)
        cursor.execute(insert_query, query_values)
        self.connection.commit()

    def truncate_table(self):
        cursor = self.connection.cursor()
        truncate_query = "TRUNCATE TABLE yle.kymenlaakso_articles"
        cursor.execute(truncate_query)
        self.connection.commit()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

class Game:
    def __init__(self, name, release_date, reviews_count, positive_reviews_percent, price, img, url):
        self.name = name
        self.release_date = release_date
        self.reviews_count = reviews_count
        self.positive_reviews_percent = positive_reviews_percent
        self.price = price
        self.img = img
        self.url = url

def find_games():
    games = []
    url = 'https://store.steampowered.com/search/?term='

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        name_elements = soup.find_all("span", class_="title")
        release_dates = soup.find_all("div", class_="col search_released responsive_secondrow")
        reviews = soup.find_all("span", class_="search_review_summary positive")
        prices = soup.find_all("div", class_="col search_discount_and_price responsive_secondrow")

        print(len(name_elements))
        print(len(reviews))
        print(len(release_dates))
        print(len(prices))

        for name_element, release_date, review, current_price in zip(name_elements, release_dates, reviews, prices):
            current_name = name_element.text
            current_release_date = release_date.text
            current_reviews_count = get_reviews_count(review["data-tooltip-html"])
            current_positive_reviews_percent = get_positive_reviews_percent(review["data-tooltip-html"])
            
            price_element = current_price.find("div", class_=["discount_final_price", "discount_final_price free"])
            
            if price_element and price_element.text == "Free":
                current_price = 0.0
            elif price_element:
                current_price = float(price_element.text.replace('\u20ac', '').replace(',', '.'))
            else:
                current_price = 0.0
            
            games.append(Game(current_name, current_release_date, current_reviews_count, current_positive_reviews_percent, current_price, None, None))
            
        return games

# Very Positive<br>87% of the 7,891,357 user reviews for this game are positive.

def get_reviews_count(text):
    start_index = text.find("of the ") + len("of the ")
    end_index = text.find(" user reviews")
    reviews_count_str = text[start_index:end_index]
    
    return float(reviews_count_str)

def get_positive_reviews_count(value):
    start_index = value.find("of the ") + len("of the ")
    end_index = value.find(" user reviews")
    reviews_count_str = value[start_index:end_index]
    
    return float(reviews_count_str)

def save_to_json(filename, games):
    if not games:
        print("Games not found. Can't save to JSON.")
        return

    with open(filename, "w", encoding="utf-8") as json_file:
        game_list = [vars(game) for game in games]
        json.dump(game_list, json_file, indent=2)

database = Database("localhost", "root", "", "webscrap")

game_list = find_games()
save_to_json("scrapers/results.json", game_list)
