import json

# Load JSON data from a file
with open('recipes.json', 'r') as file:
    data = json.load(file)

recipes = data["data"]


# for recipe in recipes:
#     print(f'{recipe["title"]}: {recipe["NER"]}')
# Prepare data for JSON
output = [{"id": i + 1, "name": recipe["title"], "ingredients": recipe["NER"], "fullRecipe": "\n".join(recipe["directions"])} for i, recipe in enumerate(recipes)]

# Save to a JSON file
with open('recipes_data.json', 'w') as file:
    json.dump(output, file, indent=4)

# Print the JSON string to console
print(json.dumps(output, indent=4))