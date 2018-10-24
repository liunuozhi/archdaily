import scrapy
from scrapy.http import Request
from archdaily.items import ArchdailyItem
from bs4 import BeautifulSoup
from pprint import pprint

class ArchdailyCrawl(scrapy.Spider):
    name = 'archdaily'
    start_urls = [
        'https://www.archdaily.com/search/projects/categories/theaters-and-performance'
    ]

    # TODO Priority test exported json file whether can be opened by pandas
    # TODO better to have IP pools

    def parse(self, response):

        # TODO Use xpath to find all category link
        BASE_URL = 'https://www.archdaily.com{0}'
        soup = BeautifulSoup(response.body, 'lxml')
        category_page = [] # project content page url collection
        for tag in soup.find_all('a', attrs={'class': 'afd-search-list__link'}):
            link = BASE_URL.format(tag['href'])
            category_page.append(link)
        for url in category_page:
            yield Request(url, callback=self.visit_project_page)

        next_url = response.css('a.next::attr(href)').extract_first()
        if next_url:
            yield Request(BASE_URL.format(next_url), callback=self.parse)

    def visit_project_page(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = ArchdailyItem()

        # project name
        item['name'] = soup.body.h1.text.strip()

        # project info
        # TODO Manufacturers cannot be parsed correctly
        info = soup.find_all('li', attrs={'class': 'afd-char-item'})
        item['info'] = [{x.h3.text.strip(): x.div.text.strip()} for x in info]

        # project description
        item['article'] = [p.text.strip() for p in soup.body.article.find_all('p')]

        yield item
