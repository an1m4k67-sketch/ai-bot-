import os
import threading
from flask import Flask
import google.generativeai as genai
import telebot

TELEGRAM_TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
# Твой текущий ключ из Google AI Studio
GEMINI_API_KEY = "AQ.Ab8RN6LC1IROZDm79AmZ_Ntsfet..."

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Настраиваем библиотеку классическим способом
genai.configure(api_key=GEMINI_API_KEY)
# Используем стабильную быструю модель
model = genai.GenerativeModel("gemini-1.5-flash")

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
  bot.reply_to(message, "Привет! 👋 Я на связи и готов отвечать.")


@bot.message_handler(func=lambda message: True)
def handle_ai(message):
  bot.send_chat_action(message.chat.id, "typing")

  try:
    # Генерируем ответ через модель
    response = model.generate_content(message.text)
    reply_text = response.text
  except Exception as e:
    reply_text = f"⚠️ Ошибка: {str(e)}"

  bot.reply_to(message, reply_text)


if __name__ == "__main__":
  t = threading.Thread(target=run_flask)
  t.start()

  print("Бот запущен...")
  bot.infinity_polling()






