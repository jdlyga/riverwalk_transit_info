from __future__ import annotations

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
import requests

@dataclass
class BusInfo:
    travelDirection: str
    travelTime: int

    def __repr__(self):
        if self.travelTime: 
            return f"{self.travelDirection}: {self.travelTime} minutes"
        else:
            return f"{self.travelDirection}: No upcoming buses"

def get_html(url):

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.binary_location = "/usr/bin/chromium-browser"

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)

    # Navigate to the website
    driver.get(url)

    # Get the HTML of the page
    html = driver.page_source

    # Close the browser
    driver.quit()

    return html

TO_NEW_YORK = "https://mybusnow.njtransit.com/bustime/wireless/html/eta.jsp?route=158&direction=New+York&id=21923&showAllBusses=on"
NJ_158 = "https://mybusnow.njtransit.com/bustime/wireless/html/eta.jsp?route=158&direction=Fort+Lee&id=26229&showAllBusses=off"

def get_bus_info(description, url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    minutes = None
    element = soup.find('strong', class_='larger', text=lambda text: text and 'MIN' in text)
    
    #template for print(f"***{description}***")
    if element:
        text = element.text.strip()
        minutes = text.split(u"\xa0")[0]
        #print(f"Next bus in {minutes} minutes")
        return minutes
    else:
        #print(f'No bus times available')
        return None

    # element = soup.find("span", class_="smaller")
    # text = element.text.strip()
    # vehicle_number = text.split(" ")[1].replace(')','')

    # print(f"Vehicle Number: {vehicle_number}")
    
    # print(vehicle_list)


def get_port_imperial_bus_info():

    to_ny_minutes = get_bus_info("Riverwalk to New York", TO_NEW_YORK)
    to_nj_minutes = get_bus_info("158 Bus to New Jersey", NJ_158)

    to_ny = BusInfo("Riverwalk to New York", to_ny_minutes)
    to_nj = BusInfo("158 Bus to New Jersey", to_nj_minutes)

    return to_ny, to_nj
