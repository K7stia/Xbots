import tweepy
import os
from flask import Flask, redirect, request, url_for
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Twitter API ключі
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Ініціалізація Flask додатку
app = Flask(__name__)

# Підключення до Twitter API через OAuth 1.0
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Підключення до Twitter через tweepy
api = tweepy.API(auth)

# Створення стартового шляху для тесту
@app.route('/')
def index():
    return "Twitter Bot is Running"

# Шлях для ініціалізації процесу OAuth
@app.route('/login')
def login():
    try:
        # Отримання URL для авторизації
        redirect_url = auth.get_authorization_url()
        return redirect(redirect_url)
    except tweepy.TweepError:
        return "Error during authentication!"

# Callback шлях після авторизації користувача
@app.route('/callback')
def callback():
    try:
        # Отримання oauth_token та oauth_verifier з URL
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')

        # Отримуємо токен доступу
        auth.get_access_token(oauth_verifier)

        # Зберігаємо токен доступу у змінних (або базі даних)
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret

        # Тепер у вас є доступ до ресурсів користувача
        user = api.me()
        return f"Authentication successful! Welcome, {user.name}!"

    except tweepy.TweepError:
        return "Error during authentication!"

# Функція для відповіді на згадки
def reply_to_mentions():
    while True:
        try:
            print("🔍 Checking for new mentions...")
            mentions = api.mentions_timeline()

            if mentions:
                print(f"Found {len(mentions)} new mentions!")
                for mention in mentions:
                    tweet_id = mention.id
                    user_id = mention.user.screen_name
                    tweet_text = mention.text
                    print(f"Processing tweet from @{user_id}: {tweet_text}")

                    # Формуємо запит до AI (заміни на свою логіку AI)
                    ai_response = f"Reply to @{user_id} with AI response: {tweet_text}"

                    # Відправка відповіді
                    api.update_status(status=ai_response, in_reply_to_status_id=tweet_id)
                    print(f"✅ Replied to @{user_id}: {ai_response}")
            else:
                print("No mentions found.")

            # Чекаємо 5 хвилин перед наступним запитом
            print("⏳ Waiting 5 minutes before next check...")
            time.sleep(30)

        except tweepy.errors.TooManyRequests:
            print("⚠️ Too many requests! Waiting 15 minutes before retrying...")
            time.sleep(90)  # Чекаємо 15 хвилин

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(30)  # Чекаємо 5 хвилин перед наступною спробою

# Запуск Flask-сервера на порту, визначеному через PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Якщо PORT не задано, використовуємо 5000 за замовчуванням
    app.run(host="0.0.0.0", port=port)
