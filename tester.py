import pickle

# stuff = {'heavy', 'pepper', 'vegetable', 'milk', 'black', 'shredded', 'onion', 'red', 'flour', 'chip', 'oil', 'semisweet', 'extract', 'skinless', 'large', 'potato', 'chopped', 'bread', 'cheddar', 'butter', 'water', 'baking', 'sliced', 'vanilla', 'cake', 'sugar', 'drained', 'fresh', 'chicken', 'soda', 'bacon', 'minced', 'grated', 'breast', 'piece', 'package', 'lemon', 'mix', 'bean', 'divided', 'needed', 'taste', 'cut', 'sauce', 'parsley', 'ground', 'cinnamon', 'mushroom', 'frozen', 'celery', 'bell', 'beaten', 'packed', 'walnut', 'cocoa', 'melted', 'brown', 'softened', 'powder', 'cheese', 'unsweetened', 'olive', 'leaf', 'cream', 'boneless', 'dried', 'egg', 'peanut', 'clove', 'peeled', 'white', 'diced', 'chocolate', 'garlic', 'green', 'tomato', 'salt', 'juice'}
# stuff = {'cherry', 'red', 'cut', 'unsalted', 'ground', 'skinless', 'frozen', 'olive', 'boneless', 'cornstarch', 'cocoa', 'cake', 'grated', 'large', 'melted', 'garlic', 'lemon', 'sweetened', 'piece', 'flour', 'orange', 'softened', 'spray', 'nutmeg', 'milk', 'banana', 'temperature', 'needed', 'water', 'black', 'cinnamon', 'crushed', 'light', 'whipped', 'small', 'cooking', 'heavy', 'seeded', 'shortening', 'baking', 'divided', 'butter', 'finely', 'bread', 'green', 'salt', 'seasoning', 'seed', 'crumb', 'taste', 'beaten', 'dry', 'pepper', 'drained', 'sliced', 'bell', 'leaf', 'oil', 'extract', 'minced', 'unsweetened', 'mix', 'chip', 'chopped', 'basil', 'powder', 'degree', 'rolled', 'oregano', 'topping', 'vanilla', 'shredded', 'crust', 'peeled', 'room', 'brown', 'packed', 'sugar', 'parsley', 'peanut', 'cayenne', 'soda', 'pie', 'semisweet', 'diced', 'half', 'vegetable', 'fresh', 'package', 'instant', 'thawed', 'oat', 'cold', 'dried', 'vinegar', 'chocolate', 'clove', 'cream', 'cumin', 'paprika', 'freshly', 'white', 'container', 'cilantro', 'sweet'}
# stuff = list(stuff)
#
# # for item in stuff:
# #     print(item)
#
fh = open('processed_recipes', 'rb')

# pickle.dump(stuff, fh)

recipes = pickle.load(fh)

print(recipes["breakfast"][2].ingredients)
# for recip in recipes:
#     for ingredient in recip.ingredients:
#         print(ingredient)
#     print("###")
