import tweepy
import openai
import os
import random
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Twitter API ключі
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Підключення до Twitter API
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Функція для отримання відповіді від GPT-4
def generate_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a crypto expert who answers Twitter mentions in a professional and engaging way. Always answer in English."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I cannot answer right now. Try again later. 😕"

# Функція для відповіді на згадку
def reply_to_mentions():
    mentions = client.get_users_mentions(id=client.get_me().data['id'])  # Отримання згадок
    if mentions.data:
        for mention in mentions.data:
            tweet_id = mention.id
            user_id = mention.author_id
            tweet_text = mention.text.lower()

            # Формуємо запит до AI
            ai_prompt = f"Reply to this tweet in an engaging, informative way about crypto & Web3: {tweet_text}"

            # Генеруємо AI-відповідь
            response = generate_ai_response(ai_prompt)

            # Надсилаємо відповідь у Twitter
            client.create_tweet(text=f"@{user_id} {response}", in_reply_to_tweet_id=tweet_id)
            print(f"Replied to @{user_id}: {response}")

# Запуск функції
if __name__ == "__main__":
    reply_to_mentions()
