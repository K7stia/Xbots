import tweepy
import openai
import os
import time
from flask import Flask
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

# Flask додаток для підтримки порту
app = Flask(__name__)

@app.route('/')
def index():
    return "Twitter Bot is Running"

# Функція для відповіді на згадки
def reply_to_mentions():
    while True:
        try:
            mentions = client.get_users_mentions(id=client.get_me().data['id'])
            if mentions.data:
                for mention in mentions.data:
                    tweet_id = mention.id
                    user_id = mention.author_id
                    tweet_text = mention.text.lower()

                    ai_prompt = f"Reply in English as a crypto expert: {tweet_text}"
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a crypto expert. Always answer in English."},
                            {"role": "user", "content": ai_prompt}
                        ]
                    )
                    ai_response = response["choices"][0]["message"]["content"].strip()

                    # Відправка відповіді
                    client.create_tweet(text=f"@{user_id} {ai_response}", in_reply_to_tweet_id=tweet_id)
                    print(f"✅ Replied to @{user_id}: {ai_response}")

            # Чекаємо 5 хвилин перед наступним запитом
            print("⏳ Waiting 5 minutes before next check...")
            time.sleep(30)

        except tweepy.errors.TooManyRequests:
            print("⚠️ Too many requests! Waiting 15 minutes before retrying...")
            time.sleep(90)  # Чекаємо **15 хвилин**

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(30)  # Чекаємо **5 хвилин** перед наступною спробою

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))  # Запуск Flask-сервера
    reply_to_mentions()
