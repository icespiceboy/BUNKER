from src.config import bot, ADMIN_ID
from src.database_mgr import db_manager

@bot.message_handler(commands=['reset'])
def reset_game_command(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, "У вас нет прав для этой команды 🔐")
        return
    db_manager.data['lobby'] = {
        "status": "CLOSED",
        "players": {}
    }

    db_manager.data['players_card'] = []
    db_manager.data['user_ordinal'] = 1

    if 'used' in db_manager.data:
        for key in db_manager.data['used']:
            db_manager.data['used'][key] = []
    else:
        db_manager.data['used'] = {
            "professions": [],
            "healths": [],
            "phobias": [],
            "hobbies": [],
            "facts": [],
            "baggages": [],
            "cards": []
        }

    db_manager.save()

    bot.send_message(message.chat.id, "<b>🧹 База данных успешно очищена!</b>\n\n"
                                      "• Лобби закрыто\n"
                                      "• Карты игроков удалены\n"
                                      "• Списки повторов сброшены\n\n"
                                      "Можно начинать новую игру с /play.", parse_mode='HTML')