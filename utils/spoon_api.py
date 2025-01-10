import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
SPOONACULAR_GET_INGREDIENTS_API_URL = os.getenv("SPOONACULAR_GET_INGREDIENTS_API_URL")
SPOONACULAR_GET_RECIPE_ID_API_URL = os.getenv("SPOONACULAR_GET_RECIPE_ID_API_URL")

def _get_spoonacular_ingredients(recipe_ids):
    params = {
        "ids": f"{','.join(recipe_ids)}",
        "apiKey": SPOONACULAR_API_KEY
    }
    try:
        # Send GET request
        response = requests.get(SPOONACULAR_GET_INGREDIENTS_API_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx

        # Parse JSON response
        recipes = response.json()
        source_urls = []
        for recipe in recipes:
            source_urls.append(recipe['sourceUrl'])
        return source_urls
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



def get_spoonacular_recipe(query, number=5):
    params = {
            "query": query,  # Search keyword
            "number": number,                      # Number of results
            "apiKey": SPOONACULAR_API_KEY     # Replace with your Spoonacular API key
        }
    response = requests.get(url=SPOONACULAR_GET_RECIPE_ID_API_URL, params=params).json()
    recipes = response.get('results', [])
    recipe_ids = []
    for recipe in recipes:
        recipe_id = f"{recipe.get('id')}"
        recipe_ids.append(recipe_id)
    return _get_spoonacular_ingredients(recipe_ids)
