import os
import threading
from flask import Flask
from google import genai
import telebot

TELEGRAM_TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
# Вставляем ключ напрямую, чтобы точно не было проблем с переменными окружения на Render
GEMINI_API_KEY = "AQ.Ab8RN6JMf0wmLjrFokiiBSnKqNenpzloIGMr1iqKkYyibVxxqw"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Мини-веб-сервер для Render
app = Flask(__name__)


@app.route("/")
def home():
  return "ИИ-Бот с Gemini работает!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "Привет! 👋 Я готов к работе. Напиши мне что-нибудь.")


@bot.message_handler(func=lambda message: True)
def handle_ai(message):
  bot.send_chat_action(message.chat.id, "typing")

  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message.text,
    )
    reply_text = response.text
  except Exception as e:
    # Ошибка выведется прямо в чат, чтобы мы сразу поняли в чем дело
    reply_text = f"⚠️ Ошибка отладки: {str(e)}"

  bot.reply_to(message, reply_text)


if __name__ == "__main__":
  t = threading.Thread(target=run_flask)
  t.start()

  print("Бот запущен...")
  bot.infinity_polling()





