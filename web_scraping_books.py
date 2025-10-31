import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


base = "http://books.toscrape.com/catalogue/page-{}.html"


rows = []

for page in range(1, 6):
    url = base.format(page)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        break
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.select("article.product_pod")

    for b in books:
        title = b.h3.a["title"].strip()
        price = b.select_one(".price_color").text.strip()
        availability = b.select_one(".availability").text.strip()
        rating = b.select_one("p")["class"][1]
        rows.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating
        })

    time.sleep(1)  # short pause to avoid overloading site

df = pd.DataFrame(rows)


df.to_csv("scraped_books.csv", index=False)
print("✅ Data saved successfully! Total books:", len(df))
