import nltk

from config import (card_classes_basic_info, card_classes_recipe_ingredients,
                    url_appendix, url_base)
from scrapers import *

scrps = {}
basic_data = []

for meal_type in list(url_appendix):
    scrps[meal_type] = (
        BasicRecipeInfoScraper(
            card_classes=card_classes_basic_info,
            meal_type=meal_type,
            url_base=url_base,
            url_appendix=url_appendix,
            limit=8,
        )
    )

ingredients = {}

for meal_type in list(scrps):
    basic_data = scrps[meal_type].scraped_data
    ingred_scrp = RecipeIngredientsScraper(
        card_classes=card_classes_recipe_ingredients, recipe_basic_infos=basic_data
    )
    ingredients[meal_type] = ingred_scrp.all_ingredients

for meal_type in list(ingredients):
    vocab = nltk.FreqDist()
    vocab.update(ingredients[meal_type])
    #
    print(meal_type)
    print('##############')
    for word, freq in vocab.most_common(30):
        print(f"{word}, {freq}")
    print('##############')