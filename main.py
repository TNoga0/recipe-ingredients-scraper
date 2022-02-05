from scrapers import *
from config import (
    url_base,
    card_classes_basic_info,
    url_appendix,
    card_classes_recipe_ingredients,
)
import nltk

scrp = BasicRecipeInfoScraper(
    card_classes=card_classes_basic_info,
    meal_type="breakfast",
    url_base=url_base,
    url_appendix=url_appendix,
    limit=10,
)

scrp_data = scrp.scraped_data
ingred_scrp = RecipeIngredientsScraper(
    card_classes=card_classes_recipe_ingredients, recipe_basic_infos=scrp_data
)

print(ingred_scrp.all_ingredients)

vocab = nltk.FreqDist()
vocab.update(ingred_scrp.all_ingredients)

for word, freq in vocab.most_common(200):
    print(f"{word}, {freq}")
