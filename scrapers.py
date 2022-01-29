from typing import Tuple
import asyncio
import re
import aiohttp
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import namedtuple

# a neat little trick - make ingredients an empty list initially and then append to that in the
# next scraper - you can do that!
ScrapedRecipeInfo = namedtuple('ScrapedRecipeInfo', 'name url image_url ingredients')


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
        return soup, url

    @abstractmethod
    def scrape_data(self, soups: Tuple):
        pass

    async def main(self):
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

    def __init__(self, card_classes={}, urls=[]):
        super().__init__(card_classes=card_classes, urls=urls)

    def scrape_data(self, soups: Tuple):
        for soup, url in soups:
            tag, class_name = self.card_classes["base"]
            nested_tags_list = soup.find_all(tag, class_=class_name)[0::2]
            for tag in nested_tags_list:
                self.scraped_data.append(ScrapedRecipeInfo(
                    tag.div.img["alt"],  # name
                    tag["href"],  # url
                    tag.div.img["src"],  # image_url
                    []  # ingredients
                ))


class RecipeIngredientsScraper(Scraper):
    """
    This class implements a scraper for recipe ingredients.
    Accepts parsed_data from Basic Info Scraper as kwarg and extends it.

    It's a child class that inherits from Scraper abc.
    """

    measurement_units = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz',
                         'gill', 'cup',
                         'c', 'cups', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal',
                         'ml', 'milliliter',
                         'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre', 'dL',
                         'bulb', 'level',
                         'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#', 'ounce', 'oz',
                         'mg',
                         'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme', 'x', 'of',
                         'mm',
                         'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre', 'inch',
                         'in', 'milli',
                         'centi', 'deci', 'hecto', 'kilo']

    stop_words = set(stopwords.words('english'))

    Lemmatizer = WordNetLemmatizer()

    def __init__(self, card_classes={}, recipe_basic_infos=[]):
        urls = list()
        self.all_ingredients = []
        self.recipe_infos = recipe_basic_infos
        for recipe in recipe_basic_infos:
            urls.append(recipe.url)
        super().__init__(card_classes=card_classes, urls=urls)
        # self.all_ingredients = set(self.all_ingredients)

    def scrape_data(self, soups: Tuple):
        for soup, url in soups:
            ingredients = []
            tag, class_name = self.card_classes["base"]
            for ingredient_tag in soup.find_all(tag, class_=class_name):
                ingredient_text = re.sub('[,]', '', ingredient_tag.text).split(' ')

                ingredient_text = [word for word in ingredient_text if word.isalpha()]
                # lemmatize words to deal with plural situation
                ingredient_text = [self.Lemmatizer.lemmatize(word) for word in ingredient_text]
                # remove measurement units
                ingredient_text = [word for word in ingredient_text if word not in self.measurement_units]
                # remove stop words (a, an, etc.)
                ingredient_text = [word for word in ingredient_text if word not in self.stop_words]
                # make words lowercase for convenience
                ingredient_text = [word.lower() for word in ingredient_text]

                self.all_ingredients.extend(ingredient_text)
                ingredients.append(" ".join(ingredient_text))
            recipe_basic_data = list(filter(lambda x: x.url == url, self.recipe_infos))[0]
            recipe_basic_data.ingredients.extend(ingredients)
            self.recipe_infos = [recipe_basic_data if recipe_basic_data.name == x.name else x for x in self.recipe_infos]
