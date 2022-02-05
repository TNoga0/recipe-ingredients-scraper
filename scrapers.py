import asyncio
import re
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Tuple, Dict, List, Union

import aiohttp
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

from utils import measurement_units

# a neat little trick - make ingredients an empty list initially and then append to that in the
# next scraper - you can do that!
ScrapedRecipeInfo = namedtuple("ScrapedRecipeInfo", "name url image_url ingredients")


class Scraper(ABC):
    """
    General abc for recipe scrapers. Base features are here, specific
    types of scraping, tag classes etc. should be provided with input args
    and main() implementation.
    """

    def __init__(self, card_classes: Dict[str, Tuple] = {}, urls: List = []) -> None:
        self.card_classes = card_classes
        self.urls = urls
        self.scraped_data = []
        asyncio.run(self.main())

    @staticmethod
    async def get_scraped_page(session: aiohttp.ClientSession, url: str) -> Tuple:
        """
        Awaits an url response, then creates BeautifulSoup object and encodes html to lxml.
        Returns a tuple of BeautifulSoup and url (url needed for proper ingredient adding,
        as the recipe data is a namedtuple)
        """
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
        return soup, url

    @abstractmethod
    def scrape_data(self, soups: Tuple) -> None:
        pass

    async def main(self) -> None:
        """
        Main method for data scraping. Asynchronously gathers scraping tasks and executes them
        """
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(self.get_scraped_page(session, url))
            soups_and_urls = await asyncio.gather(*tasks)
            self.scrape_data(soups_and_urls)


class BasicRecipeInfoScraper(Scraper):
    """
    This class implements a scraper for recipe's basic info, i.e.:
    - recipe name
    - recipe url
    - recipe image url for card view

    It's a child class that inherits from Scraper abc.
    """

    def __init__(
        self,
        card_classes: Dict[str, Tuple[str]] = {},
        meal_type: str = "",
        url_base: str = "",
        url_appendix: Dict[str, str] = {},
        limit: int = 1,
    ) -> None:
        urls = self.prepare_urls(url_base, url_appendix, meal_type, limit)
        self.url_base = url_base
        super().__init__(card_classes=card_classes, urls=urls)

    def prepare_urls(self, base: str, appendix: Dict[str, str], meal_type: str, limit: int) -> List[str]:
        """
        Prepares urls for recipe data scraping, basically adds string parts.
        """
        urls = []
        for i in range(1, limit):
            urls.append(base + appendix[meal_type] + f"?page={i}")
        return urls

    def scrape_data(self, soups: Tuple) -> None:
        """
        This one is a bit hacky/tricky. The first page of recipes is different than others. Clicking
        'load more' theoretically has the url of page 2, but navigating directly to that page
        displays something entirely different. HTML tags are different, so there's need to make a big
        'if' statement.
        The recipe infos are stored in namedtuples and the ingredients are initially an empty list.
        This allows to modify these objects in another scraper (the ingredient one).
        """
        for soup, url in soups:
            if url[-1] == "1":
                tag, class_name = self.card_classes["base"][0]
                nested_tags_list = soup.find_all(tag, class_=class_name)[0::2]
                for tag in nested_tags_list:
                    self.scraped_data.append(
                        ScrapedRecipeInfo(
                            tag.div.img["alt"],  # name
                            tag["href"],  # url
                            tag.div.img["src"],  # image_url
                            [],  # ingredients
                        )
                    )
            else:
                tag, class_name = self.card_classes["base"][1]
                nested_tags_list = soup.find_all(tag, class_=class_name)
                for tag in nested_tags_list:
                    self.scraped_data.append(
                        ScrapedRecipeInfo(
                            tag.a["title"],  # name
                            self.url_base + tag.a["href"],  # url
                            tag.a.div["data-src"],  # image_url
                            [],  # ingredients
                        )
                    )


class RecipeIngredientsScraper(Scraper):
    """
    This class implements a scraper for recipe ingredients.
    Accepts parsed_data from Basic Info Scraper as kwarg and extends it.

    It's a child class that inherits from Scraper abc.
    """

    stop_words = set(stopwords.words("english"))

    Lemmatizer = WordNetLemmatizer()

    def __init__(
        self,
        card_classes: Dict[str, Tuple] = {},
        recipe_basic_infos: List[namedtuple] = [],
        meas_units: List[str] = measurement_units,
    ) -> None:
        urls = list()
        self.measurement_units = meas_units
        self.all_ingredients = []
        self.recipe_infos = recipe_basic_infos
        for recipe in recipe_basic_infos:
            urls.append(recipe.url)
        super().__init__(card_classes=card_classes, urls=urls)
        # self.all_ingredients = set(self.all_ingredients)

    def scrape_data(self, soups: Tuple) -> None:
        """
        Gathers ingredient data by scraping and then removes unnecessary rubbish data.
        Finally, modifies the namedtuples containing recipe data and inserts them back into the list.
        """
        for soup, url in soups:
            ingredients = []
            tag, class_name = self.card_classes["base"]
            for ingredient_tag in soup.find_all(tag, class_=class_name):
                ingredient_text = re.sub("[,]", "", ingredient_tag.text).split(" ")

                ingredient_text = [word for word in ingredient_text if word.isalpha()]
                # lemmatize words to deal with plural situation
                ingredient_text = [
                    self.Lemmatizer.lemmatize(word) for word in ingredient_text
                ]
                # remove measurement units
                ingredient_text = [
                    word
                    for word in ingredient_text
                    if word not in self.measurement_units
                ]
                # remove stop words (a, an, etc.)
                ingredient_text = [
                    word for word in ingredient_text if word not in self.stop_words
                ]
                # make words lowercase for convenience
                ingredient_text = [word.lower() for word in ingredient_text]

                self.all_ingredients.extend(ingredient_text)
                ingredients.append(" ".join(ingredient_text))
            recipe_basic_data = list(filter(lambda x: x.url == url, self.recipe_infos))[0]
            recipe_basic_data.ingredients.extend(ingredients)
            self.recipe_infos = [
                recipe_basic_data if recipe_basic_data.name == x.name else x
                for x in self.recipe_infos
            ]
