import json
from crawler import Crawler

def main() -> None:
    # Initialize the Crawler and ProductInfoExtractor
    crawler = Crawler()

    # Define the URL and parameters for link extraction
    url = ""https://m.999.md/ro/list/transport/cars?page={}"
    max_pages = 3"
    pagesToProcess = 10
    pageStart = 1

    # Get links from the Crawler
    links = list(crawler.getItemsFromCategory(url, pageStart, pagesToProcess))
    crawler.push_links_to_queue('product_links_queue', links)

    num_threads = 4  # Number of concurrent consumers
    crawler.process_queue('product_links_queue', num_threads)

if __name__ == "__main__":
    main()
