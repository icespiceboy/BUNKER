from src.config import bot, CHANNEL_ID
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.database_mgr import db_manager


def generate_table_message_text():
    message_text = "📋 <b>ОБЩИЙ СТОЛ</b> 📜\n"

    for user in db_manager.data['players_card']:
        user_name = user['name']

        if user.get('is_spectator'):
            message_text += f"\n👁 <s><b>{user_name}</b></s>\n"
            continue

        user_card = user['card']['chars']
        bio_info = user_card['bio']
        user_visible = user.get('card').get('visibility')

        message_text += f"\n<b>{user_name} ({bio_info['gender']})\n</b>"

        if user_visible.get('bio', True):
            bio_info = user_card['bio']
            message_text += (
                f"<blockquote><b>БИО:</b> {bio_info['gender_name']}, "
                f"{bio_info['age']} {bio_info['years']}, "
                f"стаж работы - {bio_info['age_work']} "
                f"{bio_info['years_work']}{bio_info['fertility']}\n"
            )
        else:
            message_text += "<blockquote><b>БИО</b> ×\n"

        if user_visible.get('prof', True):
            message_text += f"<b>Профессия:</b> {user_card['prof']}\n"
        else:
            message_text += "<b>Профессия</b> ×\n"

        if user_visible.get('heal', True):
            message_text += f"<b>Здоровье:</b> {user_card['heal']}\n"
        else:
            message_text += "<b>Здоровье</b> ×\n"

        if user_visible.get('phob', True):
            message_text += f"<b>Фобия:</b> {user_card['phob']}\n"
        else:
            message_text += "<b>Фобия</b> ×\n"

        if user_visible.get('hobb', True):
            message_text += f"<b>Хобби:</b> {user_card['hobb']}\n"
        else:
            message_text += "<b>Хобби</b> ×\n"

        if user_visible.get('fact', True):
            message_text += f"<b>Факт:</b> {user_card['fact']}\n"
        else:
            message_text += "<b>Факт</b> ×\n"

        if user_visible.get('bagg', True):
            message_text += f"<b>Багаж:</b> {user_card['bagg']}\n"
        else:
            message_text += "<b>Багаж</b> ×\n"

        if user_visible.get('card1', True):
            message_text += f"<b>Карта №1:</b> {user_card['card1']}\n"
        else:
            message_text += "<b>Карта №1</b> ×\n"

        if user_visible.get('card2', True):
            message_text += f"<b>Карта №2:</b> {user_card['card2']}</blockquote>\n"
        else:
            message_text += "<b>Карта №2</b> ×</blockquote>\n"

    return message_text


def get_lobby_ui(user_id):
    lobby = db_manager.data['lobby']
    players = lobby['players']
    admin_id = "833674307"

    all_ready = True
    is_admin_in_lobby = admin_id in players

    text = "<b>🗝 Лобби выживших открыто!</b> 🧳\n\n"
    text += "<i>Чтобы попасть в бункер, подтверди готовность. Когда все будут готовы, админ начнет раздачу карт</i>\n\n"
    if is_admin_in_lobby:
        text += "<b>👥 Список группы:</b>\n"
    else:
        text += "<b>👥 Список группы:</b>\n0. Ожидаем админа ⏳\n"

    if not players:
        all_ready = False

    count = 1
    for pid, pdata in players.items():
        name = db_manager.data['all_users'].get(str(pid), "Неизвестный")

        if str(pid) == admin_id:
            status_emoji = "👑"
        else:
            status_emoji = "✅" if pdata['ready'] else "⏳"
            if not pdata['ready']:
                all_ready = False

        text += f"{count}. {name} {status_emoji}\n"
        count += 1

    text += f"\n<i>Всего участников: {len(players)}</i>"

    keyboard = InlineKeyboardMarkup()
    is_user_admin = str(user_id) == admin_id

    if is_user_admin:
        if all_ready and len(players) > 1:
            keyboard.add(InlineKeyboardButton("Начать игру 🤼‍♀️", callback_data="lobby_start"))
        keyboard.add(InlineKeyboardButton("Покинуть лобби 🚪", callback_data="lobby_leave"))
    else:
        player_data = players.get(str(user_id), {})
        is_ready = player_data.get('ready', False)

        if is_ready:
            keyboard.add(InlineKeyboardButton("В ожидание ⏳", callback_data="lobby_ready"))
        else:
            keyboard.add(InlineKeyboardButton("Приготовиться ✅", callback_data="lobby_ready"))
        keyboard.add(InlineKeyboardButton("Покинуть лобби 🚪", callback_data="lobby_leave"))

    return text, keyboard


def get_card_keyboard():
    keyboard = [
        [InlineKeyboardButton("БИО", callback_data="bio")],
        [InlineKeyboardButton("Профессия", callback_data="prof"),
         InlineKeyboardButton("Здоровье", callback_data="heal"),
         InlineKeyboardButton("Фобия", callback_data="phob")],
        [InlineKeyboardButton("Хобби", callback_data="hobb"),
         InlineKeyboardButton("Факт", callback_data="fact"),
         InlineKeyboardButton("Багаж", callback_data="bagg")],
        [InlineKeyboardButton("Карта №1", callback_data="card1"),
         InlineKeyboardButton("Карта №2", callback_data="card2")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_table_keyboard(user_id):
    keyboard = InlineKeyboardMarkup()
    admin_id = 833674307

    if int(user_id) == admin_id:
        keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="update_message"))
        keyboard.add(InlineKeyboardButton(text="Выгнать 🚪", callback_data="admin_kick_list"))
    else:
        keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="update_message"))

    return keyboard


def send_subscription_message(chat_id):
    keyboard = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton(text="🔗 BUNKER LOG!", url=f"https://t.me/{CHANNEL_ID[1:]}")
    keyboard.add(subscribe_button)
    bot.send_message(
        chat_id,
        "Проверь подписку... 📮",
        reply_markup=keyboard
    )


def get_profile_ui(user_id):
    user_id_str = str(user_id)
    user_name = db_manager.data['all_users'].get(user_id_str, "Выживший")
    text = f"📇 <b>Профиль – {user_name}</b>\n\n📡 Ваш ID: <code>{user_id}</code>\n"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сменить никнейм ✏️", callback_data="profile_change_nick"))

    lobby = db_manager.data.get('lobby', {})
    players = lobby.get('players', {})
    status = lobby.get('status', {})

    if status == "STARTED":
        text += f"🪑 <b>Статус:</b> В игре"
    elif status == "OPEN" and user_id_str in players:
        text += f"🪑 <b>Статус:</b> В лобби"
    else:
        text += "🪑 <b>Статус:</b> Вне игры"

    return text, keyboard


def send_generated_card(user_id, card_data):
    bio_data = card_data.get('chars').get('bio')
    sex = "Мужской" if bio_data.get("gender") == "М" else "Женский"

    message_text = (
        f"<b>Пол:</b> {sex}\n"
        f"× <b>БИО:</b> {bio_data.get('gender_name')}, {bio_data.get('age', 0)} "
        f"{bio_data.get('years')}, стаж работы - {bio_data.get('age_work', 0)} "
        f"{bio_data.get('years_work')}{bio_data.get('fertility')}\n\n"
        f"× <b>Профессия:</b> {card_data.get('chars').get('prof')}\n"
        f"× <b>Здоровье:</b> {card_data.get('chars').get('heal')}\n"
        f"× <b>Фобия:</b> {card_data.get('chars').get('phob')}\n"
        f"× <b>Хобби:</b> {card_data.get('chars').get('hobb')}\n"
        f"× <b>Факт:</b> {card_data.get('chars').get('fact')}\n"
        f"× <b>Багаж:</b> {card_data.get('chars').get('bagg')}\n\n"
        f"× <b>Карта №1:</b> {card_data.get('chars').get('card1')}\n"
        f"× <b>Карта №2:</b> {card_data.get('chars').get('card2')}"
    )

    reply_markup = get_card_keyboard()

    sent_message = bot.send_message(user_id, message_text, reply_markup=reply_markup, parse_mode='HTML')

    return sent_message
