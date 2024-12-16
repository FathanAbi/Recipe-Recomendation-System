import json

# Load recipe.json
with open('updated_recipes_data.json', 'r') as recipe_file:
    recipes = json.load(recipe_file)

# Load originalrecipe.json
with open('recipes.json', 'r') as original_file:
    original_data = json.load(original_file)

# Create a mapping of title to link
title_to_link = {item['title']: item['link'] for item in original_data['data']}

# Add 'link' to recipes
for recipe in recipes:
    if recipe['name'] in title_to_link:
        recipe['link'] = title_to_link[recipe['name']]
    else:
        recipe['link'] = None  # Assign None if no match is found

# Save updated recipes back to recipe.json
with open('updated_recipes_data.json', 'w') as updated_file:
    json.dump(recipes, updated_file, indent=4)

print("Updated recipes saved to updated_recipe.json")
