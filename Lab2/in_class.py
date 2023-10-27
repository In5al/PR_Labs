import requests
from bs4 import BeautifulSoup

def get_links(count,max_page,url,arr):
    origin = "https://999.md"

    response = requests.get(url)

    if response.status_code == 200:
        print("GET request successful!")

        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for link in soup.find_all('a'):
            if link.get('href') != None:
                if len(link.get('href')) > 6:
                    if link.get('href')[4].isnumeric():
                        if link.get('href') not in links:
                            links.append(link.get("href"))
                            arr.append(origin + link.get('href'))
        next_page = soup.find("li", class_="current").findNext("li")
        if max_page <= count:
            return arr
        else:
            count += 1
            url = origin + next_page.next.get('href')
            return get_links(count,max_page,url,arr)
