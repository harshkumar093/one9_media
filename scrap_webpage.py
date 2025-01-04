import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
urls=[]

def scrap_webpage(url, class_name, skip, limit):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        elements_with_class = soup.find_all(class_=class_name)
        i=0
        print(len(elements_with_class))
        for element in elements_with_class:
            if i >= skip-1:
                print(element.get('src'))
                urls.append(element.get('src'))
            i+=1
            if i-skip-1>=limit:
                break
    else:
        raise Exception(f"Failed to retrieve webpage. Status code: {response.status_code}")
    return urls
