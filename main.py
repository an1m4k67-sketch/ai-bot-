import os
import threading
from flask import Flask
from google import genai
import telebot

TELEGRAM_TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
GEMINI_API_KEY = "AQ.Ab8RN6JMf0wmLjrFokiiBSnKqNenpzloIGMr1iqKkYyibVxxqw"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Мини-веб-сервер для Render (чтобы держался порт)
app = Flask(__name__)


@app.route("/")
def home():
  return "ИИ-Бот с Gemini работает!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# Логика общения через Gemini
@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привет! 👋 Теперь я подключен к полноценной нейросети Gemini."
      " Задавай любые вопросы, пиши код или проси разобрать темы!",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(
      message,
      "Я полностью автономен и использую ИИ. Просто отправь мне сообщение!",
  )


@bot.message_handler(func=lambda message: True)
def handle_ai(message):
  # Показываем статус «печатает...», пока модель думает
  bot.send_chat_action(message.chat.id, "typing")

  try:
    # Запрос к модели Gemini 2.5 Flash
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message.text,
    )
    reply_text = response.text
  except Exception as e:
    reply_text = (
        "⚠️ Произошла ошибка при обращении к нейросети. Попробуй еще раз чуть"
        " позже."
    )

  bot.reply_to(message, reply_text)


if __name__ == "__main__":
  # Запускаем Flask в фоне
  t = threading.Thread(target=run_flask)
  t.start()

  print("Умный бот на базе Gemini запущен...")
  bot.infinity_polling()




