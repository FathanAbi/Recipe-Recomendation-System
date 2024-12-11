import json
import re

# Path to the JSON file
file_path = 'recipes_data.json'

# Open and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

pattern1 = r'\bchicken\b'
pattern2 = r'\blamb\b
pattern3 = r'\bbacon\b'
pattern4 = r'\bbacon\b''
pattern5 = r'\bbone\b'


for item in data:
    ingredients = item['ingredients']
    has_chicken = any(re.search(pattern, ingredient, re.IGNORECASE) for ingredient in ingredients)
    if has_chicken:
        print(item['name'])

