import telebot
import requests

TELEGRAM_TOKEN = '8110751447:AAGUOFYhKLOtPgOyv5oKdrdw45YK-x6a_fI'
OPENROUTER_API_KEY = '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'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_openrouter(message):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = res.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка: {e}"

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, "Привет! Я AI-ассистент. Задай мне вопрос.")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    reply = ask_openrouter(msg.text)
    bot.send_message(msg.chat.id, reply)

bot.polling()
