import asyncio
import aiohttp
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from collections import namedtuple

ScrapedRecipeInfo = namedtuple('ScrapedRecipeInfo', 'name url image_url')


class Scraper(ABC):
    """
    General abc for recipe scrapers. Base features are here, specific
    types of scraping, tag classes etc. should be provided with input args
    and main() implementation.
    """

    def __init__(self, card_classes={}, urls=[]):
        self.card_classes = card_classes
        self.urls = urls
        self.scraped_data = []
        asyncio.run(self.main())

    @staticmethod
    async def get_scraped_page(session, url):
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
        return soup

    @abstractmethod
    async def main(self):
        pass


class BasicRecipeInfoScraper(Scraper):
    """
    This class implements a scraper for recipe's basic info, i.e.:
    - recipe name
    - recipe url
    - recipe image url for card view

    It's a child class that inherits from Scraper abc.
    """

    def __init__(self, card_classes={}, urls=[]):
        super().__init__(card_classes=card_classes, urls=urls)

    async def main(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(self.get_scraped_page(session, url))
            soups = await asyncio.gather(*tasks)

            for soup in soups:
                tag, class_name = self.card_classes["base"]
                nested_tags_list = soup.find_all(tag, class_=class_name)[0::2]
                for tag in nested_tags_list:
                    self.scraped_data.append(ScrapedRecipeInfo(
                        tag.div.img["alt"],
                        tag["href"],
                        tag.div.img["src"]
                    ))
