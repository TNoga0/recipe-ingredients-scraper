from utils import unnecessary_vocab
import pickle
from config import url_appendix
from scrapers import ScrapedRecipeInfo

#open file, unpickle and then close
pickled_recipes = open("gathered_recipes", "rb")
gathered_recipes = pickle.load(pickled_recipes)
pickled_recipes.close()

meal_types = list(url_appendix)

recipes_to_process = gathered_recipes

processed_recipes = {
    "breakfast": [],
    "dessert": [],
    "main_course": [],
    "healthy": [],
}

fh = open("processed_recipes", "wb")

for meal_type in meal_types:
    for recipe in recipes_to_process[meal_type]:
        print(recipe.name)
        ingreds = recipe.ingredients
        for i, ingredient in enumerate(ingreds):
            if ingredient is not None:
                ingredient_text = ingredient.split(" ")
                ingredient_text = [word for word in ingredient_text if word not in unnecessary_vocab]
                ingredient_text = " ".join(ingredient_text)
                ingreds[i] = ingredient_text if ingredient_text != "" else None
            else:
                ingreds[i] = None
        processed_recipes[meal_type].append(ScrapedRecipeInfo(
            recipe.name,
            recipe.url,
            recipe.image_url,
            list(set(list(filter(None, ingreds))))
        ))

pickle.dump(processed_recipes, fh)
fh.close()
