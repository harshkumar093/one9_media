import requests
from bs4 import BeautifulSoup

def scrap_webpage(url, headers, class_name, skip, limit):
    print(f"Trying to scrap webpage :: url: {url}, class: {class_name}, skip: {skip}, limit: {limit}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        elements_with_class = soup.find_all(class_=class_name)
        print(f"[info] Scrapped media :: url: {url}")
        return elements_with_class
    else:
        print(f"[error] Failed to retrieve webpage. Status code: {response.status_code}")
        raise Exception(f"Failed to retrieve webpage. Status code: {response.status_code}")
