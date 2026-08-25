import os
import telebot

TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привет! Я твой ИИ-помощник на Python. Бот успешно запущен и работает"
      " 24/7!",
  )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
  bot.reply_to(message, f"Ты написал: {message.text}")


if __name__ == "__main__":
  print("Бот запущен...")
  bot.infinity_polling()
