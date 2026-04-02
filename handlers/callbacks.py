from contextlib import suppress
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.database_mgr import db_manager
from src.config import professions, facts, ADMIN_ID
from src.game_logic import update_characteristics, call_command, get_card, broadcast_lobby_update, bot
from src.ui_utils import (get_card_keyboard, generate_table_message_text, get_table_keyboard, get_profile_ui)
from src.utils import generate_message_text, check_subscription
from handlers.commands import nick_selection


@bot.callback_query_handler(func=lambda call: call.data.startswith("lobby_"))
def handle_lobby_callbacks(call):
    user_id = str(call.from_user.id)
    action = call.data.split("_")[1]
    lobby = db_manager.data['lobby']

    if action == "ready":
        lobby['players'][user_id]['ready'] = not lobby['players'][user_id]['ready']
        db_manager.save()
        broadcast_lobby_update()
        bot.answer_callback_query(call.id)

    elif action == "leave":
        if user_id in lobby['players']:
            del lobby['players'][user_id]

        if len(lobby['players']) == 0:
            lobby['status'] = 'CLOSED'

        db_manager.save()
        with suppress(Exception):
            bot.delete_message(call.message.chat.id, call.message.message_id)
        broadcast_lobby_update()
        bot.answer_callback_query(call.id, "Вы покинули лобби 🚪", show_alert=True)

    elif action == "start":
        if int(user_id) != ADMIN_ID:
            bot.answer_callback_query(call.id, "Только админ может начать игру!", show_alert=True)
            return

        bot.answer_callback_query(call.id, "Раздаю карты...")
        lobby['status'] = 'STARTED'

        for pid, pdata in lobby['players'].items():
            msg_id = pdata['lobby_message_id']
            with suppress(Exception):
                bot.edit_message_text("<b>Запуск системы... Рассылаю личные дела ⚙️</b>", chat_id=int(pid),
                                      message_id=msg_id, parse_mode='HTML')

        db_manager.data['players_card'] = []
        db_manager.data['used'] = {k: [] for k in db_manager.data['used']}

        user_ordinal = 1
        for pid, pdata in lobby['players'].items():
            card_data = get_card()

            initial_visibility = {
                "bio": False, "prof": False, "heal": False, "phob": False,
                "hobb": False, "fact": False, "bagg": False, "card1": False, "card2": False
            }

            card_text = generate_message_text(card_data['chars'], initial_visibility)
            reply_markup = get_card_keyboard()

            bot.edit_message_text(
                chat_id=int(pid),
                message_id=pdata['lobby_message_id'],
                text=card_text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )

            user_name = db_manager.data['all_users'].get(str(pid), "Unknown")

            db_manager.data['players_card'].append({
                "id": int(pid),
                "ordinal": user_ordinal,
                "name": user_name,
                "card": {
                    "chars": card_data['chars'],
                    "indexes": card_data['indexes'],
                    "visibility": initial_visibility
                },
                "card_message_id": pdata['lobby_message_id'],
                "common_message_id": 0
            })
            user_ordinal += 1

        db_manager.data['user_ordinal'] = user_ordinal
        db_manager.save()


@bot.callback_query_handler(func=lambda call: call.data in ["bio", "prof", "heal", "phob", "hobb", "fact", "bagg",
                                                            "card1", "card2"])
def update_visible_callback(call):

    user = next((user for user in db_manager.data['players_card'] if user['id'] == call.message.chat.id))

    if user:
        element_to_update = call.data

        user['card']['visibility'][element_to_update] = not \
            user['card']['visibility'][element_to_update]

        message_id = user['card_message_id']
        reply_markup = get_card_keyboard()

        new_message_text = generate_message_text(user['card']['chars'], user['card']['visibility'])

        bot.edit_message_text(new_message_text, call.message.chat.id, message_id, parse_mode='HTML',
                              reply_markup=reply_markup)

        bot.answer_callback_query(call.id, text="Статус карты обновлён ✅", show_alert=False)

        db_manager.save()


@bot.callback_query_handler(func=lambda call: call.data.startswith("profile_"))
def handle_profile_callbacks(call):
    user_id = call.from_user.id
    action = call.data.split("_")[1]

    if action == "change":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="profile_cancel"))

        nick_selection[user_id] = {
            'stage': 'awaiting_nick',
            'message_id': call.message.message_id,
            'current_nick': db_manager.data['all_users'].get(str(user_id), "Не установлен")
        }

        bot.edit_message_text(
            "💁‍♀️ Укажите свой новый никнейм:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif action == "confirm":
        user_data = nick_selection.get(user_id)
        if not user_data:
            bot.answer_callback_query(call.id, "Ошибка: данные устарели")
            return

        new_nick = user_data['nick']

        db_manager.data['all_users'][str(user_id)] = new_nick
        for player in db_manager.data['players_card']:
            if player['id'] == user_id:
                player['name'] = new_nick
                break
        db_manager.save()

        bot.answer_callback_query(call.id, f"Никнейм успешно изменен на {new_nick} ✅", show_alert=False)

        text, keyboard = get_profile_ui(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard,
                              parse_mode='HTML')

        nick_selection.pop(user_id, None)

    elif action == "edit":
        if user_id in nick_selection:
            nick_selection[user_id]['stage'] = 'awaiting_nick'

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="profile_cancel"))

        bot.edit_message_text(
            "💁‍♀️ Укажите свой новый никнейм:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif action == "cancel":
        bot.answer_callback_query(call.id, "Действие отменено ❌")

        text, keyboard = get_profile_ui(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard,
                              parse_mode='HTML')

        nick_selection.pop(user_id, None)


@bot.callback_query_handler(func=lambda call: call.data == "update_message")
def update_table_message(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        message_text = generate_table_message_text()

        for user in db_manager.data['players_card']:
            p_id = user['id']
            prev_msg_id = user.get('common_message_id')
            if prev_msg_id:
                with suppress(Exception):
                    bot.edit_message_text(message_text, p_id, prev_msg_id,
                                          parse_mode="HTML", reply_markup=get_table_keyboard(p_id))

        admin_in_players = any(u['id'] == ADMIN_ID for u in db_manager.data['players_card'])
        if user_id == ADMIN_ID and not admin_in_players:
            with suppress(Exception):
                bot.edit_message_text(message_text, ADMIN_ID, call.message.message_id,
                                      parse_mode="HTML", reply_markup=get_table_keyboard(ADMIN_ID))

        bot.answer_callback_query(call.id, "Общий стол обновлен для всех игроков! ✅")
    else:
        bot.answer_callback_query(call.id, "Чтобы обновить сообщение, подпишитесь на канал 📛", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data in ["admin_kick_list", "admin_kick_cancel"])
def handle_admin_kick_navigation(call):
    if call.from_user.id != ADMIN_ID:
        return

    if call.data == "admin_kick_cancel":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=get_table_keyboard(ADMIN_ID))
        return

    keyboard = InlineKeyboardMarkup()
    for user in db_manager.data['players_card']:
        if user.get('is_spectator'):
            continue

        if user['id'] == ADMIN_ID:
            button_text = "Себя"
        else:
            button_text = f"{user['name']}"

        keyboard.add(InlineKeyboardButton(button_text, callback_data=f"exec_kick_{user['id']}"))

    keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="admin_kick_cancel"))

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("exec_kick_"))
def handle_execute_kick(call):
    if call.from_user.id != ADMIN_ID:
        return

    target_id = int(call.data.split('_')[-1])
    lobby = db_manager.data['lobby']

    for p in db_manager.data['players_card']:
        if p['id'] == target_id:
            p['is_spectator'] = True
            break

    player_id_str = str(target_id)
    if player_id_str in lobby['players']:
        msg_id = lobby['players'][player_id_str].get('lobby_message_id')
        if msg_id:
            with suppress(Exception):
                bot.edit_message_text(
                    "<b>Вы переведены в зрители администратором 👁</b>\nТеперь вы можете только наблюдать за столом.",
                    chat_id=target_id, message_id=msg_id, parse_mode='HTML')
        del lobby['players'][player_id_str]

    active_players = [p for p in db_manager.data['players_card'] if not p.get('is_spectator')]

    if not active_players:
        lobby['status'] = 'CLOSED'
        bot.answer_callback_query(call.id, "Последний игрок удален. Игра закрыта 🔒", show_alert=True)
        bot.edit_message_text("<b>Все игроки выгнаны. Игра завершена 🛑</b>",
                              call.message.chat.id, call.message.message_id, parse_mode='HTML')
        return

    db_manager.save()
    update_table_message(call)
    bot.answer_callback_query(call.id, "Игрок переведен в зрители 👁")


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_fertility')
def cancel_fertility_callback(call):
    bot.edit_message_text("Вы отменили выбор игрока ❌", call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('generate_') or call.data == "cancel_generate")
def handle_generate_callback(call):
    if call.data == "cancel_generate":
        bot.edit_message_text("Вы отменили выбор игрока ❌", call.message.chat.id, call.message.message_id)
        return

    if call.data == "generate_all":
        message_text = "🎨 Выберите характеристику:"
        keyboard = [
            [InlineKeyboardButton("Профессия", callback_data="char_prof_all")],
            [InlineKeyboardButton("Здоровье", callback_data="char_heal_all")],
            [InlineKeyboardButton("Фобия", callback_data="char_phob_all")],
            [InlineKeyboardButton("Хобби", callback_data="char_hobb_all")],
            [InlineKeyboardButton("Факт", callback_data="char_fact_all")],
            [InlineKeyboardButton("Багаж", callback_data="char_bagg_all")],
            [InlineKeyboardButton("Отменить ❌", callback_data="cancel_generate")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
    else:
        player_id = call.data.split('_')[-1]
        message_text = "🎨 Выберите характеристику:"
        keyboard = [
            [InlineKeyboardButton("Профессия", callback_data=f"char_prof_{player_id}")],
            [InlineKeyboardButton("Здоровье", callback_data=f"char_heal_{player_id}")],
            [InlineKeyboardButton("Фобия", callback_data=f"char_phob_{player_id}")],
            [InlineKeyboardButton("Хобби", callback_data=f"char_hobb_{player_id}")],
            [InlineKeyboardButton("Факт", callback_data=f"char_fact_{player_id}")],
            [InlineKeyboardButton("Багаж", callback_data=f"char_bagg_{player_id}")],
            [InlineKeyboardButton("Отменить ❌", callback_data="cancel_generate")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id, reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('char_'))
def handle_char_callback(call):
    data = call.data.split('_')
    char, target = data[1], data[2]

    lobby_players = db_manager.data.get('lobby', {}).get('players', {})
    ids_in_game = [int(pid) for pid in lobby_players.keys()]

    if target == "all":
        for player in db_manager.data['players_card']:
            if player['id'] in ids_in_game:
                update_characteristics(player, char)

        bot.edit_message_text("Характеристики сгенерированы для всех ♻", call.message.chat.id, call.message.message_id)
    else:
        player_id = int(target)
        player = next((player for player in db_manager.data['players_card'] if player['id'] == player_id), None)
        if player:
            update_characteristics(player, char)
            bot.edit_message_text("Характеристика сгенерирована ♻", call.message.chat.id, call.message.message_id)
        else:
            bot.send_message(call.message.chat.id, "Игрок не найден 🚫🔍")


@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_fertility_'))
def remove_fertility_callback(call):
    player_id = int(call.data.split('_')[-1])

    for player in db_manager.data['players_card']:
        if player['id'] == player_id:
            fertility_status = player['card']['chars']['bio']['fertility']

            if ", неспособна рожать" in fertility_status or ", неспособен оплодотворять" in fertility_status:
                bot.edit_message_text("Последствия старости никак не убрать 👴🏻", call.message.chat.id,
                                      call.message.message_id)
            elif fertility_status == "":
                bot.edit_message_text("Менять нечего 🤰🏻💢", call.message.chat.id, call.message.message_id)
            else:
                player['card']['chars']['bio']['fertility'] = ""
                db_manager.save()

                call_command(player_id, player['card_message_id'])
                bot.edit_message_text("Готово, теперь игрок плоден! 🤰🏻", call.message.chat.id, call.message.message_id)
            break


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_player2_'))
def handle_select_player2_callback(call):
    data = call.data.split('_')
    char = data[2]
    player1_id = int(data[3])
    player2_id = int(data[4])

    player1 = next((player for player in db_manager.data['players_card'] if
                    player['id'] == player1_id), None)
    player2 = next((player for player in db_manager.data['players_card'] if
                    player['id'] == player2_id), None)

    if player1_id == player2_id:
        bot.edit_message_text("Нельзя выбирать одного и того же игрока. 👥\
        \nПопробуйте снова", call.message.chat.id, call.message.message_id)
        return

    if player1 and player2:
        if char == "prof":
            prof_index1 = player1['card']['indexes'].get(char)
            prof_index2 = player2['card']['indexes'].get(char)
            gender1 = player1['card']['chars']['bio']['gender']
            gender2 = player2['card']['chars']['bio']['gender']

            if gender1 == 'М':
                new_prof1 = professions[str(prof_index2)][0]
            else:
                if len(professions[str(prof_index2)]) > 1:
                    new_prof1 = professions[str(prof_index2)][1]
                else:
                    new_prof1 = professions[str(prof_index2)][0]
            if gender2 == 'М':
                new_prof2 = professions[str(prof_index1)][0]
            else:
                if len(professions[str(prof_index1)]) > 1:
                    new_prof2 = professions[str(prof_index1)][1]
                else:
                    new_prof2 = professions[str(prof_index1)][0]

            player1['card']['chars']['prof'] = new_prof1
            player1['card']['indexes']['prof'] = prof_index2
            player2['card']['chars']['prof'] = new_prof2
            player2['card']['indexes']['prof'] = prof_index1
        elif char == "heal":
            temp = player1['card']['chars']['heal']
            player1['card']['chars']['heal'] = player2['card']['chars']['heal']
            player2['card']['chars']['heal'] = temp
        elif char == "phob":
            temp = player1['card']['chars']['phob']
            player1['card']['chars']['phob'] = player2['card']['chars']['phob']
            player2['card']['chars']['phob'] = temp
        elif char == "hobb":
            temp = player1['card']['chars']['hobb']
            player1['card']['chars']['hobb'] = player2['card']['chars']['hobb']
            player2['card']['chars']['hobb'] = temp
        elif char == "fact":
            fact_index1 = player1['card']['indexes'].get(char)
            fact_index2 = player2['card']['indexes'].get(char)
            gender1 = player1['card']['chars']['bio']['gender']
            gender2 = player2['card']['chars']['bio']['gender']

            if gender1 == 'М':
                new_fact1 = facts[str(fact_index2)][0]
            else:
                if len(facts[str(fact_index2)]) > 1:
                    new_fact1 = facts[str(fact_index2)][1]
                else:
                    new_fact1 = facts[str(fact_index2)][0]
            if gender2 == 'М':
                new_fact2 = facts[str(fact_index1)][0]
            else:
                if len(facts[str(fact_index1)]) > 1:
                    new_fact2 = facts[str(fact_index1)][1]
                else:
                    new_fact2 = facts[str(fact_index1)][0]

            player1['card']['chars']['fact'] = new_fact1
            player1['card']['indexes']['fact'] = fact_index2
            player2['card']['chars']['fact'] = new_fact2
            player2['card']['indexes']['fact'] = fact_index1
        elif char == "bagg":
            temp = player1['card']['chars']['bagg']
            player1['card']['chars']['bagg'] = player2['card']['chars']['bagg']
            player2['card']['chars']['bagg'] = temp

        db_manager.save()

        call_command(player1_id, player1['card_message_id'])
        call_command(player2_id, player2['card_message_id'])

        bot.edit_message_text("Обмен харакетристик с учётом пола произведён успешно ♻",
                              call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(call.message.chat.id, "Один или оба игрока не найдены 🚫🔍")


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_player1_'))
def handle_select_player1_callback(call):
    data = call.data.split('_')
    char, player1_id = data[2], data[3]
    lobby_players = db_manager.data.get('lobby', {}).get('players', {})

    message_text = "2️⃣ Выберите второго игрока:"
    keyboard = []

    for player_id in lobby_players.keys():
        if str(player_id) == str(player1_id):
            continue

        player_name = db_manager.data['all_users'].get(str(player_id), f"ID: {player_id}")
        keyboard.append(
            [InlineKeyboardButton(player_name, callback_data=f"select_player2_{char}_{player1_id}_{player_id}")])

    keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id, reply_markup=reply_markup,
                          parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.startswith('swap_char_') or call.data == "cancel_swap")
def handle_swap_char_callback(call):
    if call.data == "cancel_swap":
        bot.edit_message_text("Вы отменили выбор ❌", call.message.chat.id, call.message.message_id)
        return

    char = call.data.split('_')[-1]
    lobby_players = db_manager.data.get('lobby', {}).get('players', {})

    message_text = "1️⃣ Выберите первого игрока:"
    keyboard = []

    for player_id in lobby_players.keys():
        player_name = db_manager.data['all_users'].get(str(player_id), f"ID: {player_id}")
        keyboard.append([InlineKeyboardButton(player_name, callback_data=f"select_player1_{char}_{player_id}")])

    keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
