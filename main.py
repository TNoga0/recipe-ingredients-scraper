from scrapers import *
from config import url_base, card_classes_basic_info, url_appendix, card_classes_recipe_ingredients

scrp = BasicRecipeInfoScraper(
    card_classes=card_classes_basic_info, urls=[url_base + url_appendix["breakfast"] + "?page=1",
                                                url_base + url_appendix["breakfast"] + "?page=2"]
)

scrp_data = scrp.scraped_data
ingred_scrp = RecipeIngredientsScraper(card_classes=card_classes_recipe_ingredients, recipe_basic_infos=scrp_data)
