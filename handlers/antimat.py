import random
from vkbottle.bot import Message, BotLabeler

labeler = BotLabeler()
BAD_WORDS = ["хуй", "пизд", "бля", "блять", "еб", "ёб", "сук", "муд"]
warnings = {}
processed = set()

QUOTES = [
    "«Никакое гнилое слово да не исходит из уст ваших» (Еф. 4:29).",
    "«От слов своих оправдаешься, и от слов своих осудишься» (Мф. 12:37).",
    "Сквернословие — это грех, оскверняющий душу."
]

def has_mat(text):
    return any(word in text.lower() for word in BAD_WORDS)

@labeler.private_message()
async def antimat_pm(message: Message):
    if message.id in processed: return
    processed.add(message.id)
    if not has_mat(message.text or ""): return
    await message.answer("Пожалуйста, не ругайтесь. Я православный бот и создан для доброго общения. 🙏")

@labeler.chat_message()
async def antimat_chat(message: Message):
    if message.id in processed: return
    processed.add(message.id)
    if not has_mat(message.text or ""): return

    user_id = message.from_id
    peer_id = message.peer_id
    chat_id = peer_id - 2000000000

    try:
        await message.delete()
    except Exception:
        await message.answer("⚠️ У меня нет прав на удаление сообщений.")
        return

    if peer_id not in warnings: warnings[peer_id] = {}
    count = warnings[peer_id].get(user_id, 0) + 1
    warnings[peer_id][user_id] = count

    if count == 1:
        await message.answer(f"Ваше сообщение удалено. Первое предупреждение! Общайтесь без мата.\n📖 {random.choice(QUOTES)}")
    elif count == 2:
        await message.answer(f"Ваше сообщение удалено. Последнее предупреждение!\n📖 {random.choice(QUOTES)}")
    else:
        try:
            await message.ctx_api.messages.remove_chat_user(chat_id=chat_id, user_id=user_id)
            await message.answer("Участник исключен за систематическую нецензурную лексику.")
            warnings[peer_id].pop(user_id, None)
        except Exception:
            await message.answer("Не могу исключить участника. Проверьте мои права.")
