import time
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

browser = webdriver.Chrome()
browser.get("https://www.theworlds50best.com/bars/list/1-50.html")

time.sleep(2)

we_bars: WebElement = browser.find_elements(By.CLASS_NAME, "item-bottom")

bar_names = [we.find_element(By.TAG_NAME, "h2") for we in we_bars]
bar_names_text = [bar.get_property("innerHTML") for bar in bar_names]

cities = [we.find_element(By.TAG_NAME, "p") for we in we_bars]
cities_text = [city.get_property("innerHTML") for city in cities]

pairs = list(zip(bar_names_text, cities_text))
print(list(pairs))

year = date.today().year

with open(f"data/top_bars_{year}.txt", "w", encoding="utf-8") as f:
    for index, pair in enumerate(pairs):
        f.write(f"{index+1}, {pair[0]}, {pair[1]}\n")

browser.quit()
