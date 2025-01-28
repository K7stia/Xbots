import tweepy
import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Twitter API ключі
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Аутентифікація через API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY,
                       consumer_secret=API_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

# Функція для створення твіту
def post_tweet(message):
    try:
        response = client.create_tweet(text=message)
        print(f"Tweet posted! ID: {response.data['id']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    post_tweet("Hello, world! This is my first tweet from my bot using API v2! 🚀")
