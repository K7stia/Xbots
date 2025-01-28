import tweepy
import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Twitter API ключі
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Аутентифікація через Tweepy (OAuth 2.0)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

# Функція для публікації твіту
def post_tweet(message):
    try:
        response = client.create_tweet(text=message)
        print(f"Tweet posted! ID: {response.data['id']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    post_tweet("Hello, world! This is my bot's tweet using API v2 on free plan 🚀")
