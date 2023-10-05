import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'http://127.0.0.1:8080'

def fetch_page_content(path):
    try:
        response = requests.get(f'{BASE_URL}{path}')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f'Error fetching page content: {e}')
        return None

def parse_product_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_details = {}
    fields = ["name", "author", "price", "description"]

    for field in fields:
        element = soup.find('h1', text=re.compile(fr'{field.capitalize()}:', re.IGNORECASE))
        if element:
            product_details[field] = element.find_next('h1').text.strip()

    return product_details

def extract_product_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_links = [a['href'] for a in soup.find_all('a', href=re.compile(r'^/product/\d+'))]
    return product_links

def main():
    page_paths = ['/home', '/about']
    product_list_path = '/products'

    for page_path in page_paths:
        page_html = fetch_page_content(page_path)
        if page_html:
            page_content = parse_page_content(page_html)
            print(f'{page_path} Page:\n{page_content}\n')

    product_list_html = fetch_page_content(product_list_path)
    if product_list_html:
        product_links = extract_product_links(product_list_html)
        product_dict = {}

        for product_link in product_links:
            product_html = fetch_page_content(product_link)
            if product_html:
                product_details = parse_product_details(product_html)
                product_dict[product_link] = product_details

        for product_link, product_details in product_dict.items():
            print(f'Product URL: {BASE_URL}{product_link}')
            print(json.dumps(product_details, indent=4))
            print()

if __name__ == "__main__":
    main()
