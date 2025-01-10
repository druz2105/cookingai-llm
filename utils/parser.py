import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(
    api_key=OPENAI_KEY
)


def parse_query(query):
    prompt = f"Extract the dish, ingredients, and dietary preferences from: {query}"
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=50
    )

    result = response.choices[0].text.strip()
    dish = result.split('\n')[0].replace('Dish: ', '').strip()
    return dish