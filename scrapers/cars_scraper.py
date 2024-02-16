import mysql.connector, time
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

    def insert_cars_into_database(self, game):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO webscrap.cars_car (make, model, year, mileage, price, img, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        query_values = (
            game.make,
            game.model,
            game.year,
            game.mileage,
            game.price,
            game.img,
            game.url
        )
        cursor.execute(insert_query, query_values)
        self.connection.commit()

    def truncate_table(self):
        cursor = self.connection.cursor()
        truncate_query = "TRUNCATE TABLE webscrap.cars_car"
        cursor.execute(truncate_query)
        self.connection.commit()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

class Car:
    def __init__(self, make, model, year, mileage, price, img, url):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price
        self.img = img
        self.url = url

def find_cars():
    cars = []

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:
        url = 'https://www.nettiauto.com/vaihtoautot?sortCol=enrolldate&ord=DESC&page='

        driver.get(url)
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        car_elements = soup.find_all("a", class_="childVifUrl tricky_link")
        car_images = soup.find_all("img", {'border': True})
        
        for car, image in zip(car_elements, car_images):
            current_make = car["data-make"]
            current_model = car["data-model"]
            current_year = int(car["data-year"])
            current_mileage = int(car["data-mileage"])
            current_price = int(car["data-price"])
            current_image = image["data-src"]
            current_url = car["href"]
            
            cars.append(Car(current_make, current_model, current_year, current_mileage, current_price, current_image, current_url))

    return cars

car_list = find_cars()

database = Database("localhost", "root", "", "webscrap")

database.truncate_table()

for car in car_list:
    database.insert_cars_into_database(car)

print(f'Cars scraped ({len(car_list)} found)')
