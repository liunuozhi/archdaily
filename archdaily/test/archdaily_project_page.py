import requests
from bs4 import BeautifulSoup
from pprint import pprint

def __page_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def __parse_project_data(soup):
    data = {}
    data['name'] = soup.body.h1.text.strip()
    data['article'] = [p.text.strip() for p in soup.body.article.find_all('p')]

    # project info
    info = soup.find_all('li', attrs={'class': 'afd-char-item'})
    data['info'] = [{x.h3.text.strip(): x.div.text.strip()} for x in info]

    return data


def project_page(url):
    soup = __page_content(url)
    data = __parse_project_data(soup)
    return data

if __name__ == "__main__":
    URL = 'https://www.archdaily.com/71/wall-house-far-frohnrojas'
    data = project_page(URL)
    pprint(data['article'])