import scrapy
from scrapy.http import Requests

class ArchdailyCrawl(scrapy.Spider):
    name = 'archdaily'
    start_urls = [
        'https://www.archdaily.com/search/projects/categories/theaters-and-performance'
    ]

    def parse(self, response):
        project_page = xpath.fjdklsfjslkfjdlks
        yield Request()

