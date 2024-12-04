import requests
import json
import time

# Your Pexels API key
API_KEY = "JLH8Wgq4goo4kbFq2FXdJICgri0IdmInQIa1s4e4FfyUYcHWS6GWa6tP"

# Search parameters
url = "https://api.pexels.com/v1/search"

# Load recipes data
with open('recipes_data.json', 'r') as file:
    recipes = json.load(file)

# Iterate through the recipes and query Pexels API
result_data = []  # To store results
for recipe in recipes:
    name = recipe["name"]
    print(f"Searching for: {name}")

    query_params = {
        "query": name,  # Search query
        "per_page": 1,  # Number of results
    }

    # Headers for authentication
    headers = {
        "Authorization": API_KEY
    }

    # Make the API request
    response = requests.get(url, headers=headers, params=query_params)

    # Check the response
    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos", [])
        if photos:
            # Get the first image URL
            image_url = photos[0]["src"]["original"]
            print(f"Image URL: {image_url}")
            # Add to results
            result_data.append({"name": name, "image_url": image_url})
        else:
            print("No images found.")
            result_data.append({"name": name, "image_url": None})
    else:
        print(f"Failed to fetch images. Status code: {response.status_code}, Message: {response.text}")
        result_data.append({"name": name, "image_url": None})

    # Limit requests to 2 requests per second
    time.sleep(0.5)

# Save results to a new JSON file
with open('recipes_with_images.json', 'w') as output_file:
    json.dump(result_data, output_file, indent=4)

print("Finished fetching images. Results saved to 'recipes_with_images.json'.")
