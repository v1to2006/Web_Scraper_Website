import time, json
from selenium import webdriver
from bs4 import BeautifulSoup

class Car:
    def __init__(self, make, model, year, mileage, price, url):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price
        self.url = url

def find_cars():
    cars = []

    with webdriver.Chrome() as driver:
        url = 'https://www.nettiauto.com/vaihtoautot?sortCol=enrolldate&ord=DESC&page='

        driver.get(url)
        time.sleep(0.1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        car_elements = soup.find_all("a", class_="childVifUrl tricky_link")
        
        for car in zip(car_elements):
            current_make = car["data-make"]
            current_model = car["data-model"]
            current_year = int(car["data-year"])
            current_mileage = int(car["data-mileage"])
            current_price = int(car["data-price"])
            current_url = car["href"]
            
            cars.append(Car(current_make, current_model, current_year, current_mileage, current_price, current_url))

    return cars

def save_to_json(filename):
    with open(filename, 'w') as json_file:
        car_list_data = [vars(car) for car in car_list]
        json.dump(car_list_data, json_file, indent=2)
       
        print(f"Cars results saved to {filename}")

car_list = find_cars()

save_to_json("C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/cars_results.json")

print(f'Cars scraped ({len(car_list)} found)')
