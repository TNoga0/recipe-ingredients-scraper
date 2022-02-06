url_base = "https://www.allrecipes.com"
url_appendix = {
    "breakfast": "/recipes/78/breakfast-and-brunch/",
    "dessert": "/recipes/79/desserts/",
    "main_course": "/recipes/80/main-dish/",
    "healthy": "/recipes/84/healthy-recipes/",
}
page_iterating_url = "?page="

card_classes_basic_info = {
    "base": (
        (
             "a",
             "card__titleLink manual-link-behavior elementFont__title margin-8-bottom"
        ),
        (
            "div",
            "tout__imageContainer"
        )
    ),
}

card_classes_recipe_ingredients = {"base": ("span", "ingredients-item-name")}
