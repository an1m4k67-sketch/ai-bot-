import os
import requests
import telebot

TOKEN = "8281195682:AAETwI-pZwRAkUAF_tRZmaL_8dnxRokPLfw"
bot = telebot.TeleBot(TOKEN)


def ask_ai(prompt):
  """Отправляет запрос к нейросети и возвращает ответ."""
  url = "https://text.pollinations.ai/"

  # Настройка контекста: просим нейросеть быть вежливым и умным помощником
  system_prompt = (
      "Ты — умный и дружелюбный ИИ-помощник в Telegram. Отвечай подробно,"
      " интересно и по делу на русском языке."
  )
  full_prompt = f"{system_prompt}\n\nПользователь: {prompt}\nОтвет:"

  try:
    response = requests.post(
        url,
        json={
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "model": "openai",
        },
        timeout=30,
    )
    if response.status_code == 200:
      return response.text.strip()
    else:
      return "Извини, произошла ошибка при обращении к нейросети."
  except Exception as e:
    return "Не удалось связаться с ИИ. Попробуй спросить чуть позже!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привет! 👋 Я твой личный ИИ-помощник на базе нейросети.\n\nЗадай мне"
      " любой вопрос, попроси сгенерировать идею или объяснить сложную тему!",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(
      message,
      "Просто напиши мне любое текстовое сообщение, и я отвечу тебе с помощью"
      " нейросети!",
  )


@bot.message_handler(func=lambda message: True)
def handle_ai_dialogue(message):
  # Показываем статус «печатает...» пока нейросеть думает
  bot.send_chat_action(message.chat.id, "typing")

  # Получаем ответ от ИИ
  ai_response = ask_ai(message.text)

  # Отправляем ответ пользователю
  bot.reply_to(message, ai_response)


if __name__ == "__main__":
  print("ИИ-Бот запущен...")
  bot.infinity_polling()
