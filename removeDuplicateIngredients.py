import json

# Path to the JSON file
file_path = 'recipes_data.json'

# Load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Process the data to remove duplicates and sort ingredients
for item in data:
    ingredients = item.get('ingredients', [])  # Safely get 'ingredients', defaulting to an empty list
    ingredients = list(set(ingredients))  # Remove duplicates
    ingredients = sorted(ingredients)  # Sort the ingredients
    item['ingredients'] = ingredients  # Update the item

# Path for the new JSON file
output_file_path = 'cleaned_recipes_data.json'

# Write the cleaned data to the new JSON file
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Cleaned data has been saved to {output_file_path}.")
