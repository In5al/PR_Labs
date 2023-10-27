import requests
from bs4 import BeautifulSoup
import json


def get_description(url):
    response = requests.get(url)
    if response is not None:
        soup = BeautifulSoup(response.text, 'html.parser')

    description = {}

    l1 = []
    l2 = []
    for item in soup.find_all("span", class_="adPage__content__features__key"):
        if item is not None:
            l1.append(item.text)

    for item in soup.find_all("span", class_="adPage__content__features__value"):
        if item is not None:
            l2.append(item.text)

    for index in range(len(l2)):
        description[l1[index]] = l2[index]

    extra = []
    for index in range(len(l2)+1,len(l1)):
        extra.append(index)
    description['Extra_features'] = extra

    if soup.find('h1') is not None:
        car_model = soup.find('h1').text

    des = soup.find('div', class_=("adPage__content__description grid_18"))
    if des is not None:
        description["description"] = des.text
    print(description)
    desc = {}

    desc[car_model] = description

    file_name = "description"

    with open(file_name,"a") as json_file:
        json.dump(desc, json_file)



