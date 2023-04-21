
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

url = "https://www.plus.nl/aanbiedingen"

def fetch_deals(url, driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    deals = []

    product_cards = soup.find_all("div", class_="promo")

    for product_card in product_cards:
        name = product_card.find("span", class_="promo__description").text.strip()

        price_container = product_card.find("div", class_="promo-price")
        price = float(price_container.find("span", class_="promo-price__euros").text.strip().replace(",", "."))

        discount_container = product_card.find("div", class_="promo__discount")
        discount = discount_container.text.strip() if discount_container else None

        deal = {
            "name": name,
            "price": price,
            "discount": discount,
        }

        deals.append(deal)

    return deals

if __name__ == "__main__":
    # Replace this with the path to your ChromeDriver executable
    chromedriver_path = r"C:\Users\Luc Peters\Downloads\chromedriver_win32\chromedriver.exe"

    deals = fetch_deals(url, chromedriver_path)

    # Save the data to a CSV file
    with open("plus_deals.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "price", "discount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for deal in deals:
            writer.writerow(deal)

    print("Deals saved to 'plus_deals.csv'")