import requests
from django.conf import settings

def get_nutrition(food_item):
    """
    Fetch nutritional data for a given food item from the Edamam Nutrition API.
    """
    # API endpoint and parameters
    api_url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": settings.EDAMAM_APP_ID,  # Fetch App ID from settings
        "app_key": settings.EDAMAM_APP_KEY,  # Fetch App Key from settings
        "ingr": food_item,  # Input food item
    }

    # Make the GET request to the API
    response = requests.get(api_url, params=params)

    if response.status_code == 200:  # Check if the API call is successful
        data = response.json()
        return {
            "calories": data.get("calories", 0),
            "protein": data.get("totalNutrients", {}).get("PROCNT", {}).get("quantity", 0),
            "carbs": data.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0),
            "fats": data.get("totalNutrients", {}).get("FAT", {}).get("quantity", 0),
        }
    else:
        return None 
