import time, json
from selenium import webdriver
from bs4 import BeautifulSoup

class Car:
    def __init__(self, make, model, year, mileage, price, image, url):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price
        self.image = image
        self.url = url

def find_cars(url):
    cars = []

    with webdriver.Chrome() as driver:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        car_elements = soup.find_all("a", class_="childVifUrl tricky_link")
        car_images = soup.find_all("img", { "border" : True})
        
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

def save_to_json(filename):
    with open(filename, 'w') as json_file:
        car_list_data = [vars(car) for car in car_list]
        json.dump(car_list_data, json_file, indent=2)
       
        print(f"Cars results saved to {filename}")

car_list = []

for i in range(10):
    url = f'https://www.nettiauto.com/listAdvSearchFindAgent.php?id=235868950&tb=tmp_find_agent&PN[0]=adv_search&PL[0]=advSearch.php?nwBrand=@nwBrand_model=@site=@qs=Y@id_domicile=0?id=235868950@tb=tmp_find_agent&page={i + 1}'
    
    for car in find_cars(url):
        car_list.append(car)

save_to_json("C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/cars_results.json")

print(f'Cars scraped ({len(car_list)} found)')
