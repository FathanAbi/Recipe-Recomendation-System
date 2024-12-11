import json

# Path to the JSON file
file_path = 'recipes_data.json'

# Open and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

ingredient_list = []
# Print the loaded data
for item in data:
    ingredients = item['ingredients']
    for ingredient in ingredients:
        ingredient_list.append(ingredient)

unique_list = list(set(ingredient_list))

unique_list = sorted(unique_list)
print(unique_list)  # Order may vary