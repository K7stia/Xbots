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

# Аутентифікація
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Функція для твітів
def post_tweet(message):
    api.update_status(message)
    print(f"Tweet posted: {message}")

# Приклад твітта
if __name__ == "__main__":
    post_tweet("Hello, world! This is my first tweet from my bot! 🚀")
