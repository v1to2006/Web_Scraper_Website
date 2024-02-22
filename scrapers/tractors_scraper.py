import time, json
from selenium import webdriver
from bs4 import BeautifulSoup

class Tractor:
    def __init__(self, name, price, img, url):
        self.name = name
        self.price = price
        self.img = img
        self.url = url

def find_tractors():
    tractors = []

    with webdriver.Chrome() as driver:
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

def save_to_json(filename):
    with open(filename, 'w') as json_file:
        tractor_list_data = [vars(tractor) for tractor in tractor_list]
        json.dump(tractor_list_data, json_file, indent=2)
       
        print(f"Tractors results saved to {filename}")

tractor_list = find_tractors()

save_to_json("C:/GitHub/Web/Web_Scraper_Project/Web_Scraper_Website/scrapers/results/tractors_results.json")

print(f'Tractors scraped ({len(tractor_list)} found)')