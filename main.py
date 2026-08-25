import os
import random
import telebot

TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
bot = telebot.TeleBot(TOKEN)

phrases = [
    (
        "Интересная мысль! С точки зрения логики, тут есть над чем подумать."
    ),
    (
        "Я проанализировал то, что ты написал. Давай разберем это подробнее."
    ),
    (
        "Абсолютно с тобой согласен. В таких вопросах нужен системный подход."
    ),
    "Любопытный вопрос! Могу предложить взглянуть на это под другим углом.",
]


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привет! 👋 Я твой обновленный ИИ-помощник. Готов общаться!",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(message, "Просто напиши мне любой текст, и мы начнем диалог.")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
  bot.send_chat_action(message.chat.id, "typing")
  reply = f"{random.choice(phrases)}\n\n(Твой текст: «{message.text}»)"
  bot.reply_to(message, reply)


if __name__ == "__main__":
  print("Бот запущен...")
  bot.infinity_polling()


