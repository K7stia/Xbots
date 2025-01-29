def reply_to_mentions():
    while True:
        try:
            print("🔍 Checking for new mentions...")
            mentions = client.get_users_mentions(id=client.get_me().data['id'])

            if mentions.data:
                print(f"Found {len(mentions.data)} new mentions")
                for mention in mentions.data:
                    tweet_id = mention.id
                    user_id = mention.author_id
                    tweet_text = mention.text.lower()
                    print(f"Processing tweet from @{user_id}: {tweet_text}")

                    # Формуємо запит до AI
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
            else:
                print("No mentions found")

            # Чекаємо 5 хвилин перед наступним запитом
            print("⏳ Waiting 5 minutes before next check...")
            time.sleep(30)

        except tweepy.errors.TooManyRequests:
            print("⚠️ Too many requests! Waiting 15 minutes before retrying...")
            time.sleep(90)  # Чекаємо **15 хвилин**

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(30)  # Чекаємо **5 хвилин** перед наступною спробою
