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
    
    # Number the recipe steps
    full_recipe = item.get('fullRecipe', '')
    
    # Split the recipe into steps (assuming newline separation)
    steps = full_recipe.split('\n')
    
    # Number the steps, removing any leading/trailing whitespace
    numbered_steps = [f"{i+1}. {step.strip()}" for i, step in enumerate(steps) if step.strip()]
    
    # Join the numbered steps back together
    item['fullRecipe'] = '\n'.join(numbered_steps)

# Path for the new JSON file
output_file_path = 'recipes_data.json'

# Write the cleaned data to the new JSON file
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Cleaned data has been saved to {output_file_path}.")
