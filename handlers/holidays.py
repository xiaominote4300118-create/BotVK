import aiohttp
from vkbottle.bot import Message, BotLabeler

labeler = BotLabeler()

@labeler.chat_message(text=["!праздники"])
@labeler.private_message(text=["!праздники"])
async def holidays_handler(message: Message):
    year = 2026 # Можно заменить на datetime.now().year
    # Используем открытый API для праздников (пример для России)
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/RU"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        
        text = f"📅 Праздники на {year} год (РФ):\n"
        for item in data:
            text += f"- {item['date']}: {item['localName']}\n"
        await message.answer(text)
    except Exception as e:
        await message.answer("Не удалось загрузить список праздников. Попробуйте позже.")
