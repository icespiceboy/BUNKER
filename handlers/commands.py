import random
import os
from contextlib import suppress
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.database_mgr import db_manager
from src.config import professions, CHANNEL_ID
from src.game_logic import call_command, broadcast_lobby_update, bot
from src.ui_utils import (generate_table_message_text, get_table_keyboard, get_profile_ui, get_lobby_ui,
                          send_subscription_message)
from src.utils import generate_message_text, check_subscription


@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if str(user_id) not in db_manager.data['all_users']:
        db_manager.data['all_users'][str(user_id)] = user_name
        db_manager.save()
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        message_text = ("<b>Добро пожаловать в BUNKER! 🌿🏚</b>\n\n"
                        f"Мир снаружи погиб. Прямо сейчас ты стоишь перед дверью в убежище. "
                        f"Твоя задача — выжить любой ценой и доказать остальным, что именно "
                        f"ТЫ достоин продолжить род человеческий\n\n"
                        f"<b>🎨 Твой персонаж </b>— это уникальный набор навыков, здоровья и "
                        f"странностей\n<b>⚖️ Твоя цель </b>— убедить группу не выгонять тебя на "
                        f"поверхность\n\n<b>⚠️ Вход в систему:</b>\nЧтобы "
                        f"получить доступ к управлению персонажем и командам игры, необходимо "
                        f"синхронизироваться с нашим каналом. Это твой бортовой журнал!\n\n"
                        f"<i>После подписки все функции в меню (слева внизу ≡) станут "
                        f"доступны</i>")
        keyboard = InlineKeyboardMarkup()
        url_button = InlineKeyboardButton("🔗 BUNKER LOG! — Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='HTML')
    else:
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Привет! А мы уже знакомы 😄")


@bot.message_handler(commands=['play'])
def play_command(message):
    user_id = message.from_user.id

    if not check_subscription(user_id):
        send_subscription_message(message.chat.id)
        return

    with suppress(Exception):
        bot.delete_message(message.chat.id, message.message_id)

    lobby = db_manager.data.setdefault('lobby', {'status': 'CLOSED', 'players': {}})

    if lobby['status'] == 'STARTED':
        if str(user_id) in lobby['players']:
            bot.send_message(message.chat.id, "Нельзя играть в бункер, пока ты уже в бункере 📛")
        else:
            bot.send_message(message.chat.id, "Дверь бункера уже заперта. Дождись окончания игры! ⏳")
        return

    if lobby['status'] == 'CLOSED':
        lobby['status'] = 'OPEN'

    if str(user_id) not in lobby['players']:
        is_ready_by_default = (user_id == 833674307)

        lobby['players'][str(user_id)] = {
            'ready': is_ready_by_default,
            'lobby_message_id': None
        }

        text, kb = get_lobby_ui(user_id)
        sent_msg = bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode='HTML')
        lobby['players'][str(user_id)]['lobby_message_id'] = sent_msg.message_id
        db_manager.save()

        broadcast_lobby_update()
    else:
        old_msg_id = lobby['players'][str(user_id)]['lobby_message_id']
        with suppress(Exception):
            bot.delete_message(message.chat.id, old_msg_id)

        text, kb = get_lobby_ui(user_id)
        sent_msg = bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode='HTML')
        lobby['players'][str(user_id)]['lobby_message_id'] = sent_msg.message_id
        db_manager.save()


@bot.message_handler(commands=['table'])
def table_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)

        lobby_players = db_manager.data.get('lobby', {}).get('players', {})
        admin_id = 833674307

        if str(user_id) not in lobby_players and user_id != admin_id:
            bot.send_message(message.chat.id, "Вы не в игре 😕📛")
            return

        message_text = generate_table_message_text()

        for user in db_manager.data['players_card']:
            p_id = user['id']
            prev_msg_id = user.get('common_message_id')
            kb = get_table_keyboard(p_id)

            try:
                if prev_msg_id:
                    bot.edit_message_text(message_text, p_id, prev_msg_id, parse_mode="HTML", reply_markup=kb)
                else:
                    sent = bot.send_message(p_id, message_text, parse_mode="HTML", reply_markup=kb)
                    user['common_message_id'] = sent.message_id
            except Exception:
                sent = bot.send_message(p_id, message_text, parse_mode="HTML", reply_markup=kb)
                user['common_message_id'] = sent.message_id

        admin_in_game = any(u['id'] == admin_id for u in db_manager.data['players_card'])
        if not admin_in_game:
            kb = get_table_keyboard(admin_id)
            bot.send_message(admin_id, message_text, parse_mode='HTML', reply_markup=kb)

        db_manager.save()
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['generate'])
def gen_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id != 833674307:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
            return

        lobby_players = db_manager.data.get('lobby', {}).get('players', {})

        if not lobby_players:
            bot.send_message(message.chat.id, "В лобби пока никого нет 🤷‍♂️")
            return

        message_text = "🖐 Выберите игрока (-ов):"
        player_buttons = []
        for p_id in lobby_players.keys():
            p_name = db_manager.data['all_users'].get(str(p_id), f"ID: {p_id}")
            player_buttons.append([InlineKeyboardButton(p_name, callback_data=f"generate_{p_id}")])

        keyboard = [
            [InlineKeyboardButton("Всем", callback_data="generate_all")],
            *player_buttons,
            [InlineKeyboardButton("Отменить ❌", callback_data="cancel_generate")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['shuffle'])
def shuffle_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id == 833674307:
            lobby_players = db_manager.data.get('lobby', {}).get('players', {})
            ids_in_game = [int(pid) for pid in lobby_players.keys()]

            if not ids_in_game:
                bot.send_message(message.chat.id, "Нет игроков для перемешивания 🚫")
                return

            active_players = [
                player for player in db_manager.data['players_card']
                if player['id'] in ids_in_game
            ]

            if len(active_players) < 2:
                bot.send_message(message.chat.id, "Нужно минимум 2 игрока с картами для перемешивания ♻")
                return

            original_indexes = [p["card"]["indexes"]["prof"] for p in active_players]

            max_attempts = 100
            shuffled_indexes = original_indexes[:]
            found = False
            for _ in range(max_attempts):
                random.shuffle(shuffled_indexes)
                if all(orig != shuf for orig, shuf in zip(original_indexes, shuffled_indexes)):
                    found = True
                    break

            if found:
                for i, player in enumerate(active_players):
                    new_prof_index = shuffled_indexes[i]
                    gender = player["card"]["chars"]["bio"]["gender"]

                    prof_options = professions.get(str(new_prof_index), ["Неизвестно"])

                    if gender == 'М' or len(prof_options) == 1:
                        new_prof_text = prof_options[0]
                    else:
                        new_prof_text = prof_options[1]

                    player["card"]["indexes"]["prof"] = new_prof_index
                    player["card"]["chars"]["prof"] = new_prof_text

                db_manager.save()
            else:
                bot.send_message(message.chat.id, "Не удалось перемешать профессии без совпадений 😕")
                return

            for player in active_players:
                try:
                    call_command(player['id'], player['card_message_id'])
                except Exception as e:
                    print(f"Ошибка обновления у {player['id']}: {e}")

            bot.send_message(message.chat.id, "Профессии успешно перемешаны с учётом пола ♻")
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['swap'])
def swap_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id != 833674307:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
            return

        lobby_players = db_manager.data.get('lobby', {}).get('players', {})
        if not lobby_players:
            bot.send_message(message.chat.id, "В игре пока никого нет 🤷‍♂️")
            return

        message_text = "🎨 Выберите характеристику:"
        keyboard = [
            [InlineKeyboardButton("Профессия", callback_data="swap_char_prof")],
            [InlineKeyboardButton("Здоровье", callback_data="swap_char_heal")],
            [InlineKeyboardButton("Фобия", callback_data="swap_char_phob")],
            [InlineKeyboardButton("Хобби", callback_data="swap_char_hobb")],
            [InlineKeyboardButton("Факт", callback_data="swap_char_fact")],
            [InlineKeyboardButton("Багаж", callback_data="swap_char_bagg")],
            [InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['fertility'])
def fer_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == 833674307:
            lobby_players = db_manager.data.get('lobby', {}).get('players', {})

            if not lobby_players:
                bot.send_message(message.chat.id, "В игре нет активных участников 😕📛")
                return

            message_text = "👥 Выберите игрока:"
            keyboard = []

            for player_id in lobby_players.keys():
                player_name = db_manager.data['all_users'].get(str(player_id), f"ID: {player_id}")
                keyboard.append([InlineKeyboardButton(player_name, callback_data=f"remove_fertility_{player_id}")])

            keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_fertility")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение \
            этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['shuffle'])
def shuffle_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id == 833674307:
            lobby_players = db_manager.data.get('lobby', {}).get('players', {})
            ids_in_game = [int(pid) for pid in lobby_players.keys()]

            if not ids_in_game:
                bot.send_message(message.chat.id, "Нет игроков для перемешивания 🚫")
                return

            active_players = [
                player for player in db_manager.data['players_card']
                if player['id'] in ids_in_game
            ]

            if len(active_players) < 2:
                bot.send_message(message.chat.id, "Нужно минимум 2 игрока с картами для перемешивания ♻")
                return

            original_indexes = [p["card"]["indexes"]["prof"] for p in active_players]

            max_attempts = 100
            shuffled_indexes = original_indexes[:]
            found = False
            for _ in range(max_attempts):
                random.shuffle(shuffled_indexes)
                if all(orig != shuf for orig, shuf in zip(original_indexes, shuffled_indexes)):
                    found = True
                    break

            if found:
                for i, player in enumerate(active_players):
                    new_prof_index = shuffled_indexes[i]
                    gender = player["card"]["chars"]["bio"]["gender"]

                    prof_options = professions.get(str(new_prof_index), ["Неизвестно"])

                    if gender == 'М' or len(prof_options) == 1:
                        new_prof_text = prof_options[0]
                    else:
                        new_prof_text = prof_options[1]

                    player["card"]["indexes"]["prof"] = new_prof_index
                    player["card"]["chars"]["prof"] = new_prof_text

                db_manager.save()
            else:
                bot.send_message(message.chat.id, "Не удалось перемешать профессии без совпадений 😕")
                return

            for player in active_players:
                try:
                    call_command(player['id'], player['card_message_id'])
                except Exception as e:
                    print(f"Ошибка обновления у {player['id']}: {e}")

            bot.send_message(message.chat.id, "Профессии успешно перемешаны с учётом пола ♻")
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['card'])
def card_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        user = next((player for player in db_manager.save()['players_card'] if player['id'] == user_id), None)

        if not user:
            bot.send_message(user_id, "Вы не в игре 😕📛")
            return

        card_data = user['card']

        new_message_text = generate_message_text(card_data['chars'], card_data['visibility'])
        keyboard = [
            [InlineKeyboardButton("БИО", callback_data="bio")],
            [InlineKeyboardButton("Профессия", callback_data="prof"),
             InlineKeyboardButton("Здоровье", callback_data="heal"),
             InlineKeyboardButton("Фобия", callback_data="phob")],
            [InlineKeyboardButton("Хобби", callback_data="hobb"),
             InlineKeyboardButton("Факт", callback_data="fact"),
             InlineKeyboardButton("Багаж", callback_data="bagg")],
            [InlineKeyboardButton("Карта №1", callback_data="card1"),
             InlineKeyboardButton("Карта №2", callback_data="card2")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        sent_message = bot.send_message(user_id, new_message_text, reply_markup=reply_markup, parse_mode='HTML')

        user['card_message_id'] = sent_message.message_id

        db_manager.save()
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)

        text, keyboard = get_profile_ui(user_id)

        bot.send_message(message.chat.id, text, reply_markup=keyboard,
                         parse_mode='HTML')
    else:
        send_subscription_message(message.chat.id)


# @bot.message_handler(commands=["finish"])
# def finish_handler(message):
#     try:
#         with open("database.json", "r", encoding="utf-8") as f:
#             db = json.load(f)
#
#         players_data = []
#         for player in db.get("players_card", []):
#             card = player["card"]["chars"]
#             bio = card["bio"]
#             player_data = [
#                 bio["gender_name"],
#                 f"{bio['age']} {bio['years']}",
#                 card["prof"],
#                 f"{bio['age_work']} {bio['years_work']}",
#                 card["heal"],
#                 card["phob"],
#                 card["hobb"],
#                 card["fact"],
#                 card["bagg"]
#             ]
#             players_data.append(player_data)
#
#         prompt = (
#             "Игра Бункер. Катастрофа: зомби-апокалипсис. Проанализируй персонажей
#             и выдай краткий общий итог в первой строке: победа или поражение группы. "
#             "Затем дай краткий связный текст в 2 абзацах о том, кто внёс вклад в выживание,
#             а кто мешал. Не пиши размышления. Не разделяй игроков. Не пиши длинно.\n\n"
#         )
#         for i, pdata in enumerate(players_data, 1):
#             prompt += f"Игрок {i}: {', '.join(pdata)}\n"
#
#         url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {DEEPSEEKTOKEN}"
#         }
#
#         data = {
#             "model": "deepseek-ai/DeepSeek-R1-0528",
#             "messages": [
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         }
#
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#
#         full_response = result["choices"][0]["message"]["content"]
#
#         if "</think>" in full_response:
#             full_response = full_response.split("</think>")[-1].strip()
#
#         bot.send_message(message.chat.id, full_response)
#
#     except Exception as e:
#         bot.send_message(message.chat.id, f"⚠️ Ошибка: {str(e)}")


@bot.message_handler(commands=['thriller'])
def send_circle_message(message):
    video_path = 'media/mikey.mp4'

    if os.path.exists(video_path):
        with open(video_path, 'rb') as v:
            bot.send_video_note(message.chat.id, v)
    else:
        bot.send_message(message.chat.id, "Файл видео не найден 🎥❌")


nick_selection = {}
@bot.message_handler(func=lambda msg: nick_selection.get(msg.from_user.id, {}).get('stage') == 'awaiting_nick')
def receive_nick(message):
    user_id = message.from_user.id
    new_nick = message.text

    with suppress(Exception):
        bot.delete_message(message.chat.id, message.message_id)

    user_data = nick_selection.get(user_id)
    if not user_data:
        return

    nick_selection[user_id]['nick'] = new_nick
    nick_selection[user_id]['stage'] = 'confirming'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сменить ✅", callback_data="profile_confirm"))
    keyboard.add(InlineKeyboardButton("Редактировать 📝", callback_data="profile_edit"))
    keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="profile_cancel"))

    current_nick = user_data.get('current_nick', "Не установлен")
    bot.edit_message_text(
        f"💁‍♀️ Сменить ваш текущий никнейм <b>\"{current_nick}\"</b> на новый <b>"
        f"\"{new_nick}\"</b>?\n\nПодтвердите действие:",
        message.chat.id,
        user_data['message_id'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )
