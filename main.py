import os
import random
import telebot

TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
bot = telebot.TeleBot(TOKEN)

# Варианты умных ответов для классного общения
answers = [
    "Интересный вопрос! С точки зрения технологий и логики, тут стоит учесть несколько важных факторов.",
    (
        "Я проанализировал твой запрос. Если подойти к этому креативно, то можно"
        " выделить сразу несколько крутых вариантов решения."
    ),
    (
        "Абсолютно с тобой согласен. Давай разберем это подробнее: в подобных"
        " ситуациях лучше всего действовать по шагам."
    ),
    (
        "Любопытно! Могу предложить взглянуть на это под другим углом. Что именно"
        " тебя в этом привлекает больше всего?"
    ),
]


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привет! 👋 Я твой обновленный ИИ-помощник. Теперь я полностью в строю,"
      " готов обсуждать любые темы, генерировать идеи и отвечать на вопросы!",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(
      message,
      "Просто отправь мне любой текст или вопрос, и мы сразу начнем обсуждение!",
  )


@bot.message_handler(func=lambda message: True)
def handle_dialogue(message):
  bot.send_chat_action(message.chat.id, "typing")

  text = message.text.lower()

  # Небольшие паслки на контекст общения
  if "код" in text or "программир" in text:
    reply = (
        "Код — это всегда увлекательно! На каком языке пишем или что нужно"
        " исправить?"
    )
  elif "как дела" in text or "как ты" in text:
    reply = (
        "Всё отлично, сервера на Render работают стабильно, я готов к"
        " работе!"
    )
  else:
    reply = f"{random.choice(answers)}\n\n(По поводу: «{message.text}»)"

  bot.reply_to(message, reply)


if __name__ == "__main__":
  print("Бот запущен и готов к работе...")
  bot.infinity_polling()

