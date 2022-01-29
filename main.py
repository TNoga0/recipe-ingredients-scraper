from scrapers import *
from config import url_base, card_classes_basic_info, url_appendix, card_classes_recipe_ingredients
import nltk

scrp = BasicRecipeInfoScraper(
    card_classes=card_classes_basic_info, urls=[url_base + url_appendix["breakfast"] + "?page=1",
                                                url_base + url_appendix["breakfast"] + "?page=2",
                                                url_base + url_appendix["breakfast"] + "?page=3",
                                                url_base + url_appendix["breakfast"] + "?page=6",
                                                url_base + url_appendix["breakfast"] + "?page=5",
                                                url_base + url_appendix["breakfast"] + "?page=4"]
)

scrp_data = scrp.scraped_data
ingred_scrp = RecipeIngredientsScraper(card_classes=card_classes_recipe_ingredients, recipe_basic_infos=scrp_data)

print(ingred_scrp.all_ingredients)

vocab = nltk.FreqDist()
vocab.update(ingred_scrp.all_ingredients)

for word, freq in vocab.most_common(200):
    print(f"{word}, {freq}")