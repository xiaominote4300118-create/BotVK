import time
from collections import defaultdict
from vkbottle.bot import Message, BotLabeler

labeler = BotLabeler()

# Хранилище: {peer_id: {user_id: [временные метки сообщений]}}
user_messages = defaultdict(lambda: defaultdict(list))
SPAM_LIMIT = 5      # 5 сообщений
SPAM_TIME = 10      # за 10 секунд

@labeler.chat_message()
async def antispam_handler(message: Message):
    user_id = message.from_id
    peer_id = message.peer_id
    now = time.time()

    # Очищаем старые записи
    user_messages[peer_id][user_id] = [t for t in user_messages[peer_id][user_id] if now - t < SPAM_TIME]
    user_messages[peer_id][user_id].append(now)

    # Если сообщений больше лимита - спам
    if len(user_messages[peer_id][user_id]) > SPAM_LIMIT:
        try:
            # Удаляем сообщение
            await message.delete()
            # Кикаем
            await message.ctx_api.messages.remove_chat_user(chat_id=peer_id - 2000000000, user_id=user_id)
            await message.answer("🚫 Участник исключен за флуд/спам.")
            # Очищаем историю
            user_messages[peer_id][user_id] = []
        except Exception:
            pass
