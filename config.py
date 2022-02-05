url_base = "https://www.allrecipes.com"
url_appendix = {"breakfast": "/recipes/78/breakfast-and-brunch/"}
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
    "image": (
        "div",
        "component lazy-image lazy-image-udf aspect_1x1 align-default rendered image-loaded"
    ),
}

card_classes_recipe_ingredients = {"base": ("span", "ingredients-item-name")}
