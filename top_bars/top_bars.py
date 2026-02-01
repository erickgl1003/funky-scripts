import os
import time
from datetime import date

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


# Constants
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
CURRENT_WORKSPACE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
COUNTRIES_FILE = f"{CURRENT_WORKSPACE_DIRECTORY}/data/cities_countries.txt"
TOP_BARS_FILE = f"{CURRENT_WORKSPACE_DIRECTORY}/data/top_bars_{{year}}.txt"
API_DELAY = 1
SELENIUM_DELAY = 2


def get_country(city: str) -> str | None:
    """Given a city name, returns the country it belongs to using Nominatim API."""
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "funky-scripts"}
    print(f"Fetching country for city: '{city}'")
    try:
        res = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=5)
        res.raise_for_status()
        data = res.json()
        print(f"Response data: {data}")
        if data:
            return data[0]["display_name"].split(",")[-1].strip()
        return None
    except requests.RequestException as e:
        print(f"Error fetching country for '{city}': {e}")
        return None


def generate_countries(cities: list[str]) -> dict[str, str | None]:
    """Given a list of city names, returns a dict of city->country mappings."""
    countries: dict[str, str | None] = {}
    print("Generating country data for cities:", cities )

    # Load existing data
    if os.path.exists(COUNTRIES_FILE):
        with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
            print("Loading existing city-country data")
            for line in f:
                print(line.strip())
                parts = line.strip().split(", ", 1)
                if len(parts) == 2:
                    countries[parts[0]] = parts[1]

    # Find missing cities (as set to avoid duplicates)
    cities_missing = set(city for city in cities if city not in countries)
    print("Cities missing country data:", cities_missing)

    # Fetch missing countries
    if cities_missing:
        for city in cities_missing:
            country = get_country(city)
            countries[city] = country
            time.sleep(API_DELAY)

        # Append new data
        with open(COUNTRIES_FILE, "a", encoding="utf-8") as f:
            for city in cities_missing:
                f.write(f"{city}, {countries[city]}\n")

    # Return countries in same order as input cities
    return {city: countries.get(city) for city in cities}


def scrape_top_bars() -> None:
    """Scrape top 100 bars from The World's 50 Best Bars website."""
    browser = None
    try:
        browser = webdriver.Chrome()
        browser.get("https://www.theworlds50best.com/bars/list/1-50.html")
        time.sleep(SELENIUM_DELAY)

        we_bars = browser.find_elements(By.CLASS_NAME, "item-bottom")

        bars = [we.find_element(By.TAG_NAME, "h2") for we in we_bars]
        bar_names = [bar.get_property("innerHTML") for bar in bars]

        cities = [we.find_element(By.TAG_NAME, "p") for we in we_bars]
        cities_text = [city.get_property("innerHTML") for city in cities]
        countries_eq = generate_countries(cities_text)

        output_file = TOP_BARS_FILE.format(year=date.today().year)
        with open(output_file, "w", encoding="utf-8") as f:
            for index, (name, city) in enumerate(zip(bar_names, cities_text), 1):
                country = countries_eq.get(city, "Unknown")
                f.write(f"{index}, {name}, {city}, {country}\n")

        print(f"Scraped {len(bar_names)} bars to {output_file}")

    except Exception as e:
        print(f"Error scraping top bars: {e}")

    finally:
        if browser:
            browser.quit()


if __name__ == "__main__":
    scrape_top_bars()
