import json
import re

# Path to the JSON file
file_path = 'recipes_data.json'

# Load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# List of keywords indicating animal meat
animal_meat_keywords = [
    'chicken', 'beef', 'bacon', 'lamb', 'shank', 'bone', 'pork', 'mutton', 'turkey', 
    'duck', 'ham', 'hamburger', 'sausage', 'pepperoni', 'salami', 'prosciutto', 
    'pastrami', 'fish', 'salmon', 'tuna', 'cod', 'shrimp', 'prawn', 'crab', 'lobster', 
    'anchovy', 'oyster', 'clam', 'mussel', 'venison', 'bison', 'rabbit', 'goat', 
    'kangaroo', 'chicken broth', 'beef broth', 'fish stock', 'bone broth', 'gelatin', 
    'meatball', 'meatloaf', 'kebab', 'steak', 'ribs', 'chops', 'drumstick', 'cutlet', 
    'pâté', 'meat'
]

# Compile regex pattern for case-insensitive matching
pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, animal_meat_keywords)) + r')\b', re.IGNORECASE)

# Process the data to remove duplicates, sort ingredients, and flag non-vegetarian items
for item in data:
    ingredients = item.get('ingredients', [])  # Safely get 'ingredients', defaulting to an empty list
    ingredients = list(set(ingredients))  # Remove duplicates
    ingredients = sorted(ingredients)  # Sort the ingredients
    item['ingredients'] = ingredients  # Update the item

    # Check if any ingredient matches the animal meat keywords
    if any(pattern.search(ingredient) for ingredient in ingredients):
        item['is_vegetarian'] = False
    else:
        item['is_vegetarian'] = True

# Path for the new JSON file
output_file_path = 'cleaned_recipes_data.json'

# Write the cleaned data with flags to the new JSON file
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Cleaned and flagged data has been saved to {output_file_path}.")
