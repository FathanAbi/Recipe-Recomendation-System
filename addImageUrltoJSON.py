import requests
import json
import time

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



# Path to the JSON file
file_path = 'added_image2.json'

# Open and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)


i = 0
for item in data:
    if(i >= 1000):
        break
    if(item['image_url']) == None:
        image_url = fetch_image_url(item["name"])
       
        item['image_url'] = image_url
      
        output_file_path = 'added_image2.json'

        # Write the cleaned data with flags to the new JSON file
        with open(output_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f' added {item['image_url']} to {item['id']}')
        time.sleep(5)
        
    else: 
        print(f'{item['id']} already has image_url')
    
    i+=1

output_file_path = 'added_image2.json'   
print(f"Cleaned and flagged data has been saved to {output_file_path}.")
    
    


