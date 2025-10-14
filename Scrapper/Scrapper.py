import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://koszulki.com/"
OUTPUT_CSV = "produkty.csv"
IMG_DIR = "zdjecia"
os.makedirs(IMG_DIR, exist_ok=True)
chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_soup(url):
    driver.get(url)
    time.sleep(2)
    return BeautifulSoup(driver.page_source, "html.parser")

def get_categories():
    soup = get_soup(BASE_URL)
    categories = []
    print("categorie")
    for a in soup.select("li.nav-item > a.nav-link.--l2"):
        href = a.get("href")
        if href:
            full_url = urljoin(BASE_URL, href)
            categories.append(full_url)

    return categories

def get_products_from_category(category_url):
    products = []

    return products

def main():
    all_products = []
    categories = get_categories()

    print(f"Znaleziono {len(categories)} kategorii.")

if __name__ == "__main__":
    main()
    driver.quit()