from flask import Flask, render_template, request, jsonify
import random
import json
import requests
import re


class RecipeRecommendationSystem:
    def __init__(self):
        # Expanded knowledge base of recipes
        with open('updated_recipes_data.json', 'r') as file:
            data = json.load(file)
            self.recipes = data

    def match_ingredient_query(self, ingredient, query):
        """
        Match the ingredient using a case-insensitive query-based approach
        that can handle variations like 'potatoes' and 'potato'.
        """
        # Regex pattern to match different variations of ingredients
        pattern = re.compile(r'\b' + re.escape(query) + r'\w*\b', re.IGNORECASE)
        return bool(pattern.search(ingredient))  # Check if query matches any part of the ingredient

    def recommend_recipes(self, available_ingredients, dietary_restrictions, max_cooking_time=None, excluded=None):
        """
        Main recommendation method with flexible filtering
        """
        # Convert inputs to lowercase for case-insensitive matching
        available_ingredients = [ing.lower() for ing in available_ingredients]
        excluded = [exc.lower() for exc in excluded]

        vegetarian = 'vegetarian' in dietary_restrictions
        gluten_free = 'gluten_free' in dietary_restrictions
        halal = 'halal' in dietary_restrictions

        print(excluded)

        # Filter recipes
        recommended = []
        for recipe in self.recipes:
            # Ingredient matching
            recipe_ingredients = [ing.lower() for ing in recipe['ingredients']]
            matched_ingredients = []

            # check for excluded ingredients
            excludedIngredientFound = 0
            for recipe_ingredient in recipe_ingredients:
                for exc in excluded:
                    if self.match_ingredient_query(recipe_ingredient, exc):
                        excludedIngredientFound = 1

            if excludedIngredientFound == 1:
                continue

            # Cek kecocokan bahan
            for recipe_ingredient in recipe_ingredients:
                for user_ingredient in available_ingredients:
                    if self.match_ingredient_query(recipe_ingredient, user_ingredient):
                        matched_ingredients.append(user_ingredient)

            # Hitung jumlah bahan yang cocok
            num_matched = len(matched_ingredients)
            num_recipe_ingredients = len(recipe_ingredients)  # Jumlah bahan dalam resep

            # Tentukan minimal kecocokan yang dibutuhkan
            # Misalnya, setidaknya setengah dari bahan yang dimasukkan harus ada dalam resep
            required_match = len(available_ingredients) // 2  # Setengah dari jumlah bahan yang dimasukkan

            # Tentukan persentase kecocokan berdasarkan jumlah bahan yang cocok terhadap bahan dalam resep
            match_percentage = (num_matched / num_recipe_ingredients) * 100 if num_recipe_ingredients > 0 else 0

            # Tentukan apakah jumlah bahan yang cocok memenuhi syarat minimal
            if num_matched >= required_match and match_percentage >= 20:
                # Apply filters for vegetarian
                # Dietary restriction filters
                if vegetarian and not recipe.get('is_vegetarian', False):
                    continue
                if gluten_free and not recipe.get('is_gluten_free', False):
                    continue
                if halal and not recipe.get('is_halal', False):
                    continue

                # Fallback jika tidak ada 'cooking_time' pada resep
                cooking_time = recipe.get('cooking_time', '> 20 mins')  # Default jika tidak ada

                # Ekstrak cooking time menjadi integer jika dalam format string seperti '> 20 mins'
                extracted_cooking_time = self.extract_cooking_time(cooking_time)

                # Memfilter berdasarkan max_cooking_time jika diberikan
                if max_cooking_time and extracted_cooking_time is not None:
                    if extracted_cooking_time > max_cooking_time:
                        continue

                # Tambahkan rekomendasi dengan match_percentage berdasarkan bahan resep
                recommended.append({
                    "recipe": recipe,
                    "match_percentage": match_percentage,
                    "matched_ingredients": matched_ingredients,
                })

        # Sort by match percentage
        return sorted(recommended, key=lambda x: x['match_percentage'], reverse=True)

    def extract_cooking_time(self, cooking_time_str):
        """
        Function to extract cooking time in minutes based on the string
        cooking_time_str is expected to be a string like "> 20 mins" or "> 60 mins"
        """
        # Handle cases like '> 20 mins', '> 60 mins', etc.
        if cooking_time_str:
            match = re.search(r'>\s*(\d+)\s*mins?', cooking_time_str)
            if match:
                return int(match.group(1))  # Extract the numeric part and convert to int
        return None  # Return None if the time format is not recognized


# Flask Application
app = Flask(__name__)
recipe_system = RecipeRecommendationSystem()

API_KEY = "JLH8Wgq4goo4kbFq2FXdJICgri0IdmInQIa1s4e4FfyUYcHWS6GWa6tP"
PEXELS_URL = "https://api.pexels.com/v1/search"


def fetch_image_url(recipe_name):
    headers = {"Authorization": API_KEY}
    params = {"query": recipe_name, "per_page": 1}
    response = requests.get(PEXELS_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos", [])
        if photos:
            return photos[0]["src"]["original"]  # Return the first image URL
    return None  # Fallback if no image is found


@app.route('/')
def index():
    """
    Main landing page
    """
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Recipe recommendation endpoint
    """
    # Get form data
    ingredients = request.form.get('ingredients', '').split(',')
    ingredients = [ing.strip() for ing in ingredients if ing.strip()]

    excluded = request.form.get('excluded', '').split(',')
    excluded = [exc.strip() for exc in excluded if exc.strip()]

    dietary_restrictions = request.form.getlist('dietary_restrictions')
    max_cooking_time = request.form.get('cooking_time', None)

    # Ensure max_cooking_time is an integer (if provided)
    if max_cooking_time:
        max_cooking_time = int(max_cooking_time)

    # Get recommendations
    recommendations = recipe_system.recommend_recipes(
        available_ingredients=ingredients,
        dietary_restrictions=dietary_restrictions,
        max_cooking_time=max_cooking_time,
        excluded=excluded
    )

    # Prepare response
    i = 0
    result = []
    for rec in recommendations:
        i += 1
        recipe = rec['recipe']
        image_url = recipe["image_url"]  # Fetch image URL for each recipe
        recipe["image_url"] = image_url if image_url else "/static/default-image.jpg"  # Default if no image found

        result.append({
            'id': recipe['id'],
            'name': recipe['name'],
            'ingredients': recipe['ingredients'],
            'matched_ingredients': rec['matched_ingredients'],
            'match_percentage': round(rec['match_percentage'], 2),
            'vegetarian': recipe['is_vegetarian'],
            'gluten-free': recipe['is_gluten_free'],
            'cooking_time': recipe['cooking_time'],
            'image_url': recipe['image_url'],
            'full_recipe': recipe['fullRecipe'],
        })

    return render_template('recommendations.html', recommendations=result)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    """
    Detailed recipe page
    """
    recipe = next((r for r in recipe_system.recipes if r['id'] == recipe_id), None)
    
    if recipe:
        image_url = recipe['image_url']
        recipe["image_url"] = image_url if image_url else "/static/default-image.jpg"  # Default image if not found

        # Ensure the link is absolute
        if recipe.get("link") and not recipe["link"].startswith(("http://", "https://")):
            recipe["link"] = "http://" + recipe["link"]
        
        return render_template('recipe_details.html', recipe=recipe)
    return "Recipe not found", 404

def main():
    # Ensure debug mode for development
    app.run(debug=True)


if __name__ == "__main__":
    main()
