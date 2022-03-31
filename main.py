import nltk

from config import (card_classes_basic_info, card_classes_recipe_ingredients,
                    url_appendix, url_base)
from scrapers import *

import pickle

# scrps = {
#     "breakfast": [],
#     "dessert": [],
#     "main_course": [],
#     "healthy": [],
# }
basic_data = []
indie = []
ingredients = {
    "breakfast": [],
    "dessert": [],
    "main_course": [],
    "healthy": [],
}
unnecessary_words_set = set()

recipes_to_be_pickled = {
    "breakfast": [],
    "dessert": [],
    "main_course": [],
    "healthy": [],
}

fh = open('scraped_basic_infos', 'rb')

#
# for lim in range(0, 30, 6):
#     for meal_type in list(url_appendix):
#         scrps[meal_type].append(
#             BasicRecipeInfoScraper(
#                 card_classes=card_classes_basic_info,
#                 meal_type=meal_type,
#                 url_base=url_base,
#                 url_appendix=url_appendix,
#                 limit_start=1+lim,
#                 limit_end=6+lim,
#             )
#         )
#
# pickle.dump(scrps, fh)
# fh.close()


scrps = pickle.load(fh)
fh.close()
print(scrps)

for meal_type in list(scrps):
    for scraper in scrps[meal_type]:
    # print(scrps[meal_type].scraped_data)
        basic_data = scraper.scraped_data
        ingred_scrp = RecipeIngredientsScraper(
            card_classes=card_classes_recipe_ingredients, recipe_basic_infos=basic_data
        )
        ingredients[meal_type].extend(ingred_scrp.all_ingredients)
        # indie.extend(ingred_scrp.all_ingredients)
        # to_be_pickled.extend(ingred_scrp.recipe_infos)
        recipes_to_be_pickled[meal_type].extend(ingred_scrp.recipe_infos)
#
#
#

fh = open('gathered_recipes', 'wb')
try:
    pickle.dump(recipes_to_be_pickled, fh)
except:
    pass

# for meal_type in list(ingredients):
#     vocab = nltk.FreqDist()
#     vocab.update(ingredients[meal_type])
#     #
#     print(meal_type)
#     print('##############')
#     for word, freq in vocab.most_common(50):
#         print(f"{word}, {freq}")
#         unnecessary_words_set.add(word)
#     print('##############')




# try:
#     pickle.dump(to_be_pickled, fh)
# except:
#     pass
# vocab = nltk.FreqDist()
# vocab.update(indie)
# for word, freq in vocab.most_common(200):
#     print(f"{word}, {freq}")
#     unnecessary_words_set.add(word)
# print(unnecessary_words_set)