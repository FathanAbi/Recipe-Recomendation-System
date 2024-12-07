# app.py
from flask import Flask, render_template, request, jsonify
import random
import json
import requests


class RecipeRecommendationSystem:
    def __init__(self):
        # Expanded knowledge base of recipes
        with open('recipes_data.json', 'r') as file:
            data = json.load(file)
            self.recipes = data


    
    def recommend_recipes(self, 
                          available_ingredients
                          ):
        """
        Main recommendation method with flexible filtering
        """
        # Convert inputs to lowercase for case-insensitive matching
        available_ingredients = [ing.lower() for ing in available_ingredients]
        
        # Filter recipes
        recommended = []
        for recipe in self.recipes:
            # Ingredient matching
            recipe_ingredients = [ing.lower() for ing in recipe['ingredients']]
            matched_ingredients = set(recipe_ingredients) & set(available_ingredients)
            # Calculate match percentage with additional flexibility
            if len(recipe_ingredients) > 0:
                match_percentage = len(matched_ingredients) / len(recipe_ingredients) * 100
            else:
                match_percentage = 0
            
            # # Apply filters
            # dietary_match = (not dietary_restrictions) or \
            #                 (dietary_restrictions == ['none']) or \
            #                 any(rest in recipe['dietary_restrictions'] for rest in dietary_restrictions)
            
            # time_match = recipe['cooking_time'] <= max_cooking_time
            
            # skill_hierarchy = {
            #     "beginner": ["beginner"],
            #     "intermediate": ["beginner", "intermediate"],
            #     "advanced": ["beginner", "intermediate", "advanced"]
            # }
            # skill_match = recipe['skill_level'] in skill_hierarchy.get(skill_level, [])
            
            # # If all conditions met
            if match_percentage >= 20:
                recommended.append({
                    "recipe": recipe,
                    "match_percentage": match_percentage,
                    "matched_ingredients": list(matched_ingredients)
                })
        
        # Sort by match percentage
        return sorted(recommended, key=lambda x: x['match_percentage'], reverse=True)

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
    
    # dietary_restrictions = request.form.getlist('dietary_restrictions')
    # max_cooking_time = int(request.form.get('cooking_time', 60))
    # skill_level = request.form.get('skill_level', 'beginner')
    
    # Get recommendations
    recommendations = recipe_system.recommend_recipes(
        available_ingredients=ingredients,
        # dietary_restrictions=dietary_restrictions,
        # max_cooking_time=max_cooking_time,
        # skill_level=skill_level
    )
    
    # Prepare response
    result = []
    for rec in recommendations:
        recipe = rec['recipe']
        image_url = fetch_image_url(recipe["name"])  # Fetch image URL for each recipe
        recipe["image_url"] = image_url if image_url else "/static/default-image.jpg"  # Default if no image found
        
        result.append({
            'id': recipe['id'],
            'name': recipe['name'],
            'ingredients': recipe['ingredients'],
            'matched_ingredients': rec['matched_ingredients'],
            'match_percentage': round(rec['match_percentage'], 2),
            # 'cooking_time': recipe['cooking_time'],
            # 'skill_level': recipe['skill_level'],
            # 'cuisine': recipe['cuisine'],
            'image_url': recipe['image_url'],
            'full_recipe': recipe['fullRecipe'],
            # 'nutrition': recipe['nutrition']
        })
    
    return render_template('recommendations.html', recommendations=result)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    """
    Detailed recipe page
    """
    recipe = next((r for r in recipe_system.recipes if r['id'] == recipe_id), None)
    #Fetch image URL based on recipe name
    image_url = fetch_image_url(recipe["name"])
    recipe["image_url"] = image_url if image_url else "/static/default-image.jpg"  # Default image if not found

    if recipe:
        return render_template('recipe_details.html', recipe=recipe)
    return "Recipe not found", 404

def main():
    # Ensure debug mode for development
    app.run(debug=True)

if __name__ == "__main__":
    main()