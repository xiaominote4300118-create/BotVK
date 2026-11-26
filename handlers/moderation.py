import re
from vkbottle.bot import Message, BotLabeler

labeler = BotLabeler()
chat_data = {} # Хранилище: {peer_id: {"warns": {}, "bans": [], "rules": "текст"}}

def get_target_id(message: Message):
    """Ищет ID пользователя в упоминании @ или в ответе на сообщение"""
    # Если ответ на сообщение
    if message.reply_message:
        return message.reply_message.from_id
    # Если упоминание через @
    match = re.search(r'\[id(\d+)\|', message.text or "")
    if match:
        return int(match.group(1))
    return None

@labeler.chat_message(text=["!варн"])
async def warn_user(message: Message):
    target_id = get_target_id(message)
    if not target_id:
        await message.answer("Укажите пользователя через @ или ответьте на его сообщение.")
        return
    
    peer_id = message.peer_id
    if peer_id not in chat_data: chat_data[peer_id] = {"warns": {}, "bans": [], "rules": ""}
    
    warns = chat_data[peer_id]["warns"]
    count = warns.get(target_id, 0) + 1
    warns[target_id] = count

    if count >= 3:
        try:
            await message.ctx_api.messages.remove_chat_user(chat_id=peer_id - 2000000000, user_id=target_id)
            await message.answer(f"Участник [id{target_id}|пользователь] исключен (3/3 предупреждения).")
            warns.pop(target_id, None)
        except Exception:
            await message.answer("Не удалось исключить. Проверьте права.")
    else:
        await message.answer(f"Участнику [id{target_id}|пользователь] выдано предупреждение ({count}/3).")

@labeler.chat_message(text=["!распред"])
async def unwarn_user(message: Message):
    target_id = get_target_id(message)
    if not target_id:
        await message.answer("Укажите пользователя через @ или ответьте на его сообщение.")
        return
    
    peer_id = message.peer_id
    if peer_id in chat_data and target_id in chat_data[peer_id]["warns"]:
        chat_data[peer_id]["warns"].pop(target_id)
        await message.answer(f"С пользователя [id{target_id}|пользователь] сняты все предупреждения.")
    else:
        await message.answer("У этого пользователя нет предупреждений.")

@labeler.chat_message(text=["!правила"])
async def set_rules(message: Message):
    # Если просто "!правила" - показать
    if len(message.text.split()) == 1:
        rules = chat_data.get(message.peer_id, {}).get("rules")
        await message.answer(f"📜 Правила беседы:\n{rules}" if rules else "Правила еще не установлены.")
    # Если "!правила текст..." - установить
    else:
        new_rules = message.text[len("!правила "):]
        if message.peer_id not in chat_data: chat_data[message.peer_id] = {"warns": {}, "bans": [], "rules": ""}
        chat_data[message.peer_id]["rules"] = new_rules
        await message.answer("✅ Правила беседы обновлены.")

@labeler.chat_message(text=["!бан"])
async def ban_user(message: Message):
    target_id = get_target_id(message)
    if not target_id: return
    
    try:
        await message.ctx_api.messages.remove_chat_user(chat_id=message.peer_id - 2000000000, user_id=target_id)
        if message.peer_id not in chat_data: chat_data[message.peer_id] = {"warns": {}, "bans": [], "rules": ""}
        chat_data[message.peer_id]["bans"].append(target_id)
        await message.answer("Участник забанен.")
    except Exception:
        await message.answer("Не удалось забанить. Проверьте права.")

@labeler.chat_message(text=["!баны"])
async def list_bans(message: Message):
    bans = chat_data.get(message.peer_id, {}).get("bans", [])
    if not bans:
        await message.answer("Список забаненных пуст.")
        return
    
    text = "🚫 Забаненные участники:\n"
    for uid in bans:
        text += f"- [id{uid}|пользователь]\n"
    await message.answer(text)
