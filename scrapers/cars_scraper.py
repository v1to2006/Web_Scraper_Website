import time, json
from selenium import webdriver
from bs4 import BeautifulSoup

class Car:
    def __init__(self, make, model, year, mileage, price, img, url):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price
        self.img = img
        self.url = url

def find_cars(url):
    cars = []

    with webdriver.Chrome() as driver:
        driver.get(url)
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        car_elements = soup.find_all("a", class_="childVifUrl tricky_link")
        car_images = soup.find_all("img", { "border" : "0"})
        
        for car, img in zip(car_elements, car_images):
            current_make = car["data-make"]
            current_model = car["data-model"]
            current_year = int(car["data-year"])
            current_mileage = int(car["data-mileage"])
            current_price = int(car["data-price"])
            current_img = img["data-src"]
            current_url = car["href"]
            
            cars.append(Car(current_make, current_model, current_year, current_mileage, current_price, current_img, current_url))

    return cars

def save_to_json(filename):
    with open(filename, 'w') as json_file:
        car_list_data = [vars(car) for car in car_list]
        json.dump(car_list_data, json_file, indent=2)
       
        print(f"Cars results saved to {filename}")

car_list = []

for i in range(10):
    url = f'https://www.nettiauto.com/vaihtoautot?pfrom=5000&pto=75000&id_country[]=73&page={i + 1}'
    
    for car in find_cars(url):
        car_list.append(car)

save_to_json("C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/cars_results.json")

print(f'Cars scraped ({len(car_list)} found)')
