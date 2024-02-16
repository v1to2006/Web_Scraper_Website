import mysql.connector, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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

    def insert_tractors_into_database(self, tractor):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO webscrap.tractors_tractor (name, price, img, url) VALUES (%s, %s, %s, %s)"
        query_values = (
            tractor.name,
            tractor.price,
            tractor.img,
            tractor.url
        )
        cursor.execute(insert_query, query_values)
        self.connection.commit()

    def truncate_table(self):
        cursor = self.connection.cursor()
        truncate_query = "TRUNCATE TABLE webscrap.tractors_tractor"
        cursor.execute(truncate_query)
        self.connection.commit()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

class Tractor:
    def __init__(self, name, price, img, url):
        self.name = name
        self.price = price
        self.img = img
        self.url = url

def find_tractors():
    tractors = []

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:
        url = 'https://www.nettikone.com/maatalouskoneet/traktorit?id_country[]=73'

        driver.get(url)
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        tractor_elements = soup.find_all("a", class_="childVifUrl tricky_link")
        tractor_prices = soup.find_all("div", class_="main_price")
        tractor_images = soup.find_all("img", {'border': True})
        
        for tractor_element, price, image in zip(tractor_elements, tractor_prices, tractor_images):
            current_name = tractor_element.text
            
            if price.text.replace('\u20ac', '').replace(' ', '') == "Eihinnoiteltu":
                current_price = 0
            else:
                current_price = float(price.text.replace('\u20ac', '').replace(' ', ''))
            
            current_image = image["data-src"]
            current_url = tractor_element["href"]
            
            tractors.append(Tractor(current_name, current_price, current_image, current_url))

    return tractors

tractor_list = find_tractors()

database = Database("localhost", "root", "", "webscrap")

database.truncate_table()

for tractor in tractor_list:
    database.insert_tractors_into_database(tractor)

print(f'Tractors scraped ({len(tractor_list)} found)')