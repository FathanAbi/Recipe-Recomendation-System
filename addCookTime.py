import json
import re

# Fungsi untuk mengekstrak dan menjumlahkan waktu dari instruksi (baik menit maupun jam)
def extract_and_sum_cooking_time(instructions):
    # Regex untuk menangkap waktu dalam menit atau jam
    matches = re.findall(r'(\d+)\s*(minute|min|mins|minutes|hour|hours|h)', instructions.lower())
    
    total_minutes = 0
    
    # Loop melalui semua waktu yang ditemukan
    for match in matches:
        time_value = int(match[0])  # Ambil nilai angka
        unit = match[1]  # Ambil unit (minute, hour, dll.)
        
        if "hour" in unit or "h" == unit:  # Konversi jam ke menit
            total_minutes += time_value * 60
        else:
            total_minutes += time_value  # Jika dalam menit, tambahkan langsung
    
    return total_minutes if total_minutes > 0 else None

# Fungsi untuk mengklasifikasikan waktu berdasarkan kategori
def classify_time(minutes):
    if minutes <= 5:
        return "> 5 mins"
    elif minutes <= 10:
        return "> 10 mins"
    elif minutes <= 20:
        return "> 20 mins"
    elif minutes <= 40:
        return "> 40 mins"
    elif minutes <= 60:
        return "> 60 mins"
    else:
        return "> 120 mins"

# Fungsi untuk memperkirakan kategori waktu memasak berdasarkan instruksi
def estimate_cooking_time(recipe_name, ingredients, instructions):
    cooking_time_from_instructions = extract_and_sum_cooking_time(instructions)
    
    if cooking_time_from_instructions is not None:
        return classify_time(cooking_time_from_instructions)
    
    cooking_time_by_instruction = check_keywords_in_instructions(instructions)
    
    if cooking_time_by_instruction is not None:
        return cooking_time_by_instruction
    
    return estimate_by_recipe_type(recipe_name, ingredients, instructions)

# Fungsi untuk mengecek kata kunci dalam instruksi dan menentukan kategori waktu
def check_keywords_in_instructions(instructions):
    instructions = instructions.lower()
    
    if "grill" in instructions or "grilled" in instructions:
        return "> 40 mins"
    elif "roast" in instructions or "bake" in instructions:
        return "> 40 mins"
    elif "fry" in instructions or "stir-fry" in instructions:
        return "> 20 mins"
    elif "simmer" in instructions or "boil" in instructions:
        return "> 20 mins"
    elif "salad" in instructions or "smoothie" in instructions:
        return "> 5 mins"
    elif "steam" in instructions:
        return "> 20 mins"
    elif "slow cook" in instructions or "stew" in instructions:
        return "> 120 mins"
    elif "microwave" in instructions:
        return "> 10 mins"
    
    return None

# Fungsi untuk memperkirakan waktu berdasarkan nama resep atau bahan
def estimate_by_recipe_type(recipe_name, ingredients, instructions):
    if 'salad' in recipe_name.lower() or 'smoothie' in recipe_name.lower():
        return "> 5 mins"
    elif 'roast' in recipe_name.lower() or 'stew' in recipe_name.lower():
        return "> 40 mins"
    elif 'grill' in recipe_name.lower() or 'bbq' in recipe_name.lower():
        return "> 40 mins"
    elif 'stir-fry' in recipe_name.lower() or 'fry' in recipe_name.lower():
        return "> 20 mins"
    elif 'soup' in recipe_name.lower():
        return "> 20 mins"
    elif 'slow cook' in recipe_name.lower():
        return "> 120 mins"
    else:
        return "> 20 mins"

# Membaca data resep dari file JSON
with open('recipes_data.json', 'r') as file:
    recipes_data = json.load(file)

# Proses untuk menambahkan kategori waktu ke setiap resep
for recipe in recipes_data:
    estimated_time = estimate_cooking_time(recipe['name'], recipe['ingredients'], recipe['fullRecipe'])
    recipe['cooking_time'] = estimated_time

# Simpan data resep yang telah diperbarui ke file JSON baru
with open('updated_recipes_data.json', 'w') as file:
    json.dump(recipes_data, file, indent=4)

print("Waktu memasak telah ditambahkan ke setiap resep dalam kategori waktu.")
