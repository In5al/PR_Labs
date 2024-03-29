
import requests
import json
from bs4 import BeautifulSoup

def crawling(url, max_num_page=None, start_page=1):
    parsed_links = []

    while max_num_page is None or start_page <= max_num_page:
        response = requests.get(url.format(start_page))

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select(".block-items__item__title")

            for link in links:
                href = link.get("href")
                if href and "/booster/" not in href:
                    parsed_links.append("https://999.md" + href)

            next_page_links = soup.select(".pagination__item--next a")
            if not next_page_links:
                break

            start_page += 1
        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code}")
            break

    return parsed_links

if __name__ == "__main__":
    url_template = "https://m.999.md/ro/list/transport/cars?page={}"
    max_pages = 3
    parsed_links = crawling(url_template, max_num_page=max_pages)

    with open("parsed_links.json", "w") as json_file:
        json.dump(parsed_links, json_file, indent=4)

    print(f"Parsed links have been saved to 'parsed_links.json'")
