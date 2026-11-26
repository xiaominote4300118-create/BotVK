import datetime
from vkbottle.bot import Message, BotLabeler

labeler = BotLabeler()

# Ключевые слова для приветствия
GREETING_WORDS = ["привет", "здравствуйте", "добрый день", "добрый вечер", "доброе утро", "приветствую"]

@labeler.private_message(text=GREETING_WORDS)
async def private_greeting_handler(message: Message):
    # Определяем время суток
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        time_greeting = "Доброе утро"
        blessing = "Божьего благословения на этот день"
    elif 12 <= hour < 17:
        time_greeting = "Добрый день"
        blessing = "хорошего дня"
    elif 17 <= hour < 23:
        time_greeting = "Добрый вечер"
        blessing = "спокойного вечера"
    else:
        time_greeting = "Здравствуйте"
        blessing = "доброй ночи"

    text = (
        f"{time_greeting}! {blessing}! 🙏\n\n"
        f"Я автоматический бот этого сообщества. Пожалуйста, напишите свой вопрос, "
        f"и администратор ответит вам, как только освободится."
    )
    await message.answer(text)
