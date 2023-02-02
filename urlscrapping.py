# -*- coding: utf-8 -*-
"""

Created on Thu Feb  2 21:11:56 2023

@author: Aditya King
"""

import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_info(url):
    # Send GET request to the URL
    response = requests.get(url)
    # Initialize the variable 'products' with an empty list
    products = []
    # Check if the request was successful
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract the relevant information for each product
        for product in soup.find_all("div", class_="s-result-item"):
            product_info = {}
            product_link = product.find("a", class_="a-link-normal")
            product_info["product_url"] = product_link["href"] if product_link else None
            product_name = product.find("span", class_="a-size-medium a-color-base a-text-normal")
            product_info["product_name"] = product_name.text if product_name else None
            product_price = product.find("span", class_="a-offscreen")
            product_info["product_price"] = product_price.text if product_price else None
            rating = product.find("span", class_="a-icon-alt")
            product_info["rating"] = rating.text.split(" ")[0] if rating else None
            review_count = product.find("span", class_="a-size-base s-underline-text")
            product_info["review_count"] = review_count.text.strip() if review_count else None
            products.append(product_info)
    return products


# Scrape 20 pages of product listings
products = []
for i in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&page={i}&qid=1653308124&ref=sr_pg_{i}"
    products.extend(scrape_product_info(url))

# Define the headers for the CSV file
headers = ["product_url", "product_name", "product_price", "rating", "review_count"]

# Open a CSV file for writing with UTF-8 encoding
with open("products.csv", "w", newline="", encoding="UTF-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    # Write the headers to the CSV file
    writer.writeheader()
    # Write the scraped product information to the CSV file
    for product in products:
        writer.writerow(product)


