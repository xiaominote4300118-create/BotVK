import os
from vkbottle.bot import Bot

from handlers.greetings import labeler as greetings_labeler
from handlers.antimat import labeler as antimat_labeler
from handlers.moderation import labeler as moderation_labeler
from handlers.holidays import labeler as holidays_labeler
from handlers.antispam import labeler as antispam_labeler

token = os.getenv("API_TOKEN")
bot = Bot(token=token)

bot.labeler.load(greetings_labeler)
bot.labeler.load(antimat_labeler)
bot.labeler.load(moderation_labeler)
bot.labeler.load(holidays_labeler)
bot.labeler.load(antispam_labeler)

if __name__ == "__main__":
    print("Бот запущен!")
    bot.run_forever()
