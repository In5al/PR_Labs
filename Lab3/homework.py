import requests
import json
from bs4 import BeautifulSoup

def extract_product_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("header", class_="adPage__header").text.strip()
        
        price_element = soup.find("span", class_="adPage__content__price-feature__prices__price__value")
        currency_element = soup.find("span", class_="adPage__content__price-feature__prices__price__currency")
        
        price = price_element.text.strip() if price_element else None
        currency = currency_element.text.strip() if currency_element else None

        seller = soup.find("dl", class_="adPage__aside__stats__owner").text.strip()
        description = soup.find("div", class_="adPage__content__description grid_18").text.strip()
        characteristics = soup.find("div", class_="adPage__content__features__col grid_9 suffix_1").text.strip()
        region = soup.find("dl", class_="adPage__content__region grid_18").text.strip()

        product_details = {
            "Title": title,
            "Price": f"{price} {currency}" if price and currency else None,
            "Seller": seller,
            "Description": description,
            "Characteristics": characteristics,
            "Region": region,
        }

        return product_details

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the product page: {e}")
        return None

if __name__ == "__main__":
    url = "https://999.md/ro/84212119"
    details = extract_product_details(url)

    if details:
        json_details = json.dumps(details, indent=4, ensure_ascii=False)
        print(json_details)
