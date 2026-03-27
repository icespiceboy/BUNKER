import json
import random
import os
from dotenv import load_dotenv
from contextlib import suppress
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

with open('database.json', 'r', encoding='utf-8') as db_in:
    database = json.load(db_in)

def save_database():
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=4)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


professions = load_json('array_prof.json')
healths = load_json('array_heal.json')
phobias = load_json('array_phob.json')
hobbies = load_json('array_hobb.json')
facts = load_json('array_fact.json')
baggages = load_json('array_bagg.json')
cards = load_json('array_card.json')

load_dotenv()
CHANNEL_ID = '@bunkernewss'
bot = telebot.TeleBot(os.getenv('TELEGRAMTOKEN'))


def check_subscription(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка check_subscription: {e}")
        return False


def send_subscription_message(chat_id):
    keyboard = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton(text="🔗 BUNKER LOG!", url=f"https://t.me/{CHANNEL_ID[1:]}")
    keyboard.add(subscribe_button)
    bot.send_message(
        chat_id,
        "Проверь подписку... 📮",
        reply_markup=keyboard
    )


@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if str(user_id) not in database['all_users']:
        database['all_users'][str(user_id)] = user_name
        save_database()
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


def get_years(age):
    last_digit = age % 10
    if 10 < age < 20 or last_digit == 0 or 5 <= last_digit <= 9:
        return 'лет'
    elif last_digit == 1:
        return 'год'
    else:
        return 'года'


def get_years_work(age_work):
    last_digit = age_work % 10
    if 10 < age_work < 20 or last_digit == 0 or 5 <= last_digit <= 9:
        return 'лет'
    elif last_digit == 1:
        return 'год'
    else:
        return 'года'


def get_profession(gender):
    used_professions = database['used']['professions']

    while True:
        profession_index = random.choice(list(professions.keys()))
        if profession_index not in used_professions:
            if gender == "М":
                profession = professions[profession_index][0]
            else:
                if len(professions[profession_index]) > 1:
                    profession = professions[profession_index][1]
                else:
                    profession = professions[profession_index][0]
            used_professions.append(profession_index)
            return profession, profession_index


def get_health(gender):
    used_healths = database['used']['healths']

    while True:
        health_index = random.choice(list(healths.keys()))
        if health_index not in used_healths:
            health = healths[health_index][0]
            used_healths.append(health_index)
            break

    if random.random() <= 0.25:
        health = "Идеальное"
        health_status = ""
    else:
        if health == "Импотенция" and gender == 'Ж':
            health = "Идеальное"
            health_status = ""
        else:
            if health in ("Плоскостопие", "Альцгеймер (передаётся по наследству с 50% шансом)",
                          "Гемофилия (нарушение свертываемости крови, передаётся по наследству)",
                          "Глаукома (повышенное внутриглазное давление, передаётся по наследству с 50% шансом)",
                          "Деменция", "Дальтонизм (передаётся по наследству с 50% шансом)", "Умственная отсталость",
                          "Цинга (слабость, заболевание дёсен)", "Врожденная нечувствительность к боли",
                          "Повышенная регенерация",
                          "Ускоренный метаболизм (передаётся по наследству с 50% шансом)",
                          "Замедленный метаболизм (передаётся по наследству с 50% шансом)"):
                health_status = random.choice([
                    "(Степень тяжести - 10%)",
                    "(Степень тяжести - 20%)",
                    "(Степень тяжести - 30%)",
                    "(Степень тяжести - 40%)",
                    "(Степень тяжести - 50%)",
                    "(Степень тяжести - 60%)",
                    "(Степень тяжести - 70%)",
                    "(Степень тяжести - 80%)",
                    "(Степень тяжести - 90%)",
                    "(Степень тяжести - 100%)"])
            else:
                if health in ("Отсутствие ноги", "Отсутствие руки", "Полная глухонемота", "Раздвоение личности",
                              "Импотенция", "Паранойя", "СПИД"):
                    health_status = ""
                else:
                    if health in ("Рак крови (Группа - C)", "Рак молочной железы (Группа - А)",
                                  "Рак лёгких (Группа - B)", "Рак кожи (Группа - А)", "Рак желудка (Группа - B)",
                                  "Мышечная дистрофия (передаётся по наследству)"):
                        health_status = random.choice(["(Стадия - Ⅰ)", "(Стадия - Ⅱ)", "(Стадия - Ⅲ)", "(Стадия - Ⅳ)"])
                    else:
                        if health == "Ожирение":
                            health_status = random.choice(["(Стадия - Ⅰ)", "(Стадия - Ⅱ)", "(Стадия - Ⅲ)"])

                        else:
                            if health == "Сахарный диабет":
                                health_status = random.choice([
                                    "(Врождённый)",
                                    "(Приобретённый)"])
                            else:
                                health_status = random.choice([
                                    "(Степень тяжести - инкубационный период)",
                                    "(Степень тяжести - инкубационный период)",
                                    "(Степень тяжести - 10%)",
                                    "(Степень тяжести - 20%)",
                                    "(Степень тяжести - 30%)",
                                    "(Степень тяжести - 40%)",
                                    "(Степень тяжести - 50%)",
                                    "(Степень тяжести - 60%)",
                                    "(Степень тяжести - 70%)",
                                    "(Степень тяжести - 80%)",
                                    "(Степень тяжести - 90%)",
                                    "(Степень тяжести - 100%)",
                                    "(Степень тяжести - ремиссия)",
                                    "(Степень тяжести - ремиссия)"
                                ])

    return health, health_status, health_index


def get_phobia():
    used_phobias = database['used']['phobias']

    while True:
        phobia_index = random.choice(list(phobias.keys()))
        if phobia_index not in used_phobias:
            phobia = phobias[phobia_index][0]
            used_phobias.append(phobia_index)
            break

    return phobia, phobia_index


def get_hobby():
    used_hobbies = database['used']['hobbies']

    while True:
        hobby_index = random.choice(list(hobbies.keys()))
        if hobby_index not in used_hobbies:
            hobby = hobbies[hobby_index][0]
            used_hobbies.append(hobby_index)
            break

    return hobby, hobby_index


def get_fact(gender):
    used_facts = database['used']['facts']

    while True:
        fact_index = random.choice(list(facts.keys()))
        if fact_index not in used_facts:
            fact = facts[fact_index][0] if gender == "М" else facts[fact_index][1]
            used_facts.append(fact_index)
            return fact, fact_index


def get_baggage():
    used_baggages = database['used']['baggages']

    while True:
        baggage_index = random.choice(list(baggages.keys()))
        if baggage_index not in used_baggages:
            baggage = baggages[baggage_index][0]
            used_baggages.append(baggage_index)
            break

    return baggage, baggage_index


def get_card():
    random1 = random.random()
    gender = 'М' if random1 < 0.5 else 'Ж'

    random2 = random.random()
    if random2 < 0.4:
        age = random.randint(18, 29)
    elif random2 < 0.7:
        age = random.randint(30, 40)
    elif random2 < 0.9:
        age = random.randint(41, 55)
    else:
        age = random.randint(56, 80)

    if age <= 25:
        gender_name = "Парень" if gender == "М" else "Девушка"
    elif age <= 35:
        gender_name = "Молодой человек" if gender == "М" else "Девушка"
    elif age <= 59:
        gender_name = "Мужчина" if gender == "М" else "Женщина"
    else:
        gender_name = "Пожилой мужчина" if gender == "М" else "Пожилая женщина"

    if gender == "М":
        if age <= 65:
            fertility = ', бесплоден' if random.random() <= 0.1 else ''
        else:
            fertility = ", неспособен оплодотворять"
    else:
        if age <= 48:
            fertility = ', бесплодна' if random.random() <= 0.1 else ''
        else:
            fertility = ", неспособна рожать"

    age_work = random.randint(0, age - 18)
    years = get_years(age)
    years_work = get_years_work(age_work)

    profession, profession_index = get_profession(gender)
    health, health_status, health_index = get_health(gender)
    phobia, phobia_index = get_phobia()
    hobby, hobby_index = get_hobby()
    fact, fact_index = get_fact(gender)
    baggage, baggage_index = get_baggage()

    used_cards = database['used']['cards']

    while True:
        card1_index = random.choice(list(cards.keys()))
        if card1_index not in used_cards:
            card1 = cards[card1_index][0]
            break

    while True:
        card2_index = random.choice(list(cards.keys()))
        if card2_index != card1_index and card2_index not in used_cards:
            card2 = cards[card2_index][0]
            break

    database['used']['cards'].extend([card1_index, card2_index])

    card_data = {
        "chars": {
            "bio": {
                "gender": gender,
                "gender_name": gender_name,
                "age": age,
                "years": years,
                "age_work": age_work,
                "years_work": years_work,
                "fertility": fertility
            },
            "prof": profession,
            "heal": f"{health} {health_status}",
            "phob": phobia,
            "hobb": hobby,
            "fact": fact,
            "bagg": baggage,
            "card1": card1,
            "card2": card2,
        },
        "indexes": {
            "prof": profession_index,
            "heal": health_index,
            "phob": phobia_index,
            "hobb": hobby_index,
            "fact": fact_index,
            "bagg": baggage_index,
            "card1": card1_index,
            "card2": card2_index
        },
        "visibility": {
            "bio": False,
            "prof": False,
            "heal": False,
            "phob": False,
            "hobb": False,
            "fact": False,
            "bagg": False,
            "card1": False,
            "card2": False
        }
    }

    return card_data


def get_lobby_ui(user_id):
    lobby = database['lobby']
    players = lobby['players']

    text = "<b>🗝 Лобби выживших открыто!</b> 🧳\n\n"
    text += "<i>Чтобы попасть в бункер, подтверди готовность. Когда все будут готовы, админ начнет раздачу карт</i>\n\n"
    text += "<b>👥 Список группы:</b>\n"

    all_ready = True
    count = 1

    for pid, pdata in players.items():
        name = database['all_users'].get(str(pid), "Неизвестный")

        if int(pid) == 833674307:
            status_emoji = "👑"
        else:
            status_emoji = "🟢" if pdata['ready'] else "⏳"
            if not pdata['ready']:
                all_ready = False

        text += f"{count}. {name} {status_emoji}\n"
        count += 1

    text += f"\n<i>Всего участников: {len(players)}</i>"

    keyboard = InlineKeyboardMarkup()
    is_admin = int(user_id) == 833674307

    if is_admin:
        if all_ready and len(players) > 1:
            keyboard.add(InlineKeyboardButton("Начать игру 🤼‍♀️", callback_data="lobby_start"))
        keyboard.add(InlineKeyboardButton("Покинуть лобби 🚪", callback_data="lobby_leave"))
    else:
        is_ready = players.get(str(user_id), {}).get('ready', False)
        if is_ready:
            keyboard.add(InlineKeyboardButton("Я не готов 🔴", callback_data="lobby_ready"))
        else:
            keyboard.add(InlineKeyboardButton("Я готов 🟢", callback_data="lobby_ready"))
        keyboard.add(InlineKeyboardButton("Покинуть лобби 🚪", callback_data="lobby_leave"))

    return text, keyboard


def broadcast_lobby_update():
    for pid, pdata in database['lobby']['players'].items():
        msg_id = pdata.get('lobby_message_id')
        if msg_id:
            text, kb = get_lobby_ui(pid)
            with suppress(Exception):
                bot.edit_message_text(text, chat_id=int(pid), message_id=msg_id, reply_markup=kb, parse_mode='HTML')


@bot.message_handler(commands=['play'])
def play_command(message):
    user_id = message.from_user.id

    if not check_subscription(user_id):
        send_subscription_message(message.chat.id)
        return

    with suppress(Exception):
        bot.delete_message(message.chat.id, message.message_id)

    lobby = database.setdefault('lobby', {'status': 'CLOSED', 'players': {}})

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
        save_database()

        broadcast_lobby_update()
    else:
        old_msg_id = lobby['players'][str(user_id)]['lobby_message_id']
        with suppress(Exception):
            bot.delete_message(message.chat.id, old_msg_id)

        text, kb = get_lobby_ui(user_id)
        sent_msg = bot.send_message(message.chat.id, text, reply_markup=kb, parse_mode='HTML')
        lobby['players'][str(user_id)]['lobby_message_id'] = sent_msg.message_id
        save_database()


@bot.callback_query_handler(func=lambda call: call.data.startswith("lobby_"))
def handle_lobby_callbacks(call):
    user_id = str(call.from_user.id)
    action = call.data.split("_")[1]
    lobby = database['lobby']

    if action == "ready":
        lobby['players'][user_id]['ready'] = not lobby['players'][user_id]['ready']
        save_database()
        broadcast_lobby_update()
        bot.answer_callback_query(call.id)

    elif action == "leave":
        if user_id in lobby['players']:
            del lobby['players'][user_id]

        if len(lobby['players']) == 0:
            lobby['status'] = 'CLOSED'

        save_database()
        with suppress(Exception):
            bot.delete_message(call.message.chat.id, call.message.message_id)
        broadcast_lobby_update()
        bot.answer_callback_query(call.id, "Вы покинули лобби 🚪", show_alert=True)

    elif action == "start":
        if int(user_id) != 833674307:
            bot.answer_callback_query(call.id, "Только админ может начать игру!", show_alert=True)
            return

        bot.answer_callback_query(call.id, "Раздаю карты...")
        lobby['status'] = 'STARTED'

        for pid, pdata in lobby['players'].items():
            msg_id = pdata['lobby_message_id']
            with suppress(Exception):
                bot.edit_message_text("<b>Запуск системы... Рассылаю личные дела ⚙️</b>", chat_id=int(pid),
                                      message_id=msg_id, parse_mode='HTML')

        database['players_card'] = []
        database['used'] = {k: [] for k in database['used']}

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

            user_name = database['all_users'].get(str(pid), "Unknown")

            database['players_card'].append({
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

        database['user_ordinal'] = user_ordinal
        save_database()


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


@bot.callback_query_handler(func=lambda call: call.data in ["bio", "prof", "heal", "phob", "hobb", "fact", "bagg",
                                                            "card1", "card2"])
def update_visible_callback(call):

    user = next((user for user in database['players_card'] if user['id'] == call.message.chat.id))

    if user:
        element_to_update = call.data

        user['card']['visibility'][element_to_update] = not \
            user['card']['visibility'][element_to_update]

        message_id = user['card_message_id']
        reply_markup = get_card_keyboard()

        new_message_text = generate_message_text(user['card']['chars'], user['card']['visibility'])

        bot.edit_message_text(new_message_text, call.message.chat.id, message_id, parse_mode='HTML', reply_markup=reply_markup)

        bot.answer_callback_query(call.id, text="Статус карты обновлён ✅", show_alert=False)

        save_database()


def call_command(chat_id, message_id):
    user = next((user for user in database['players_card'] if user['card_message_id'] == message_id), None)

    if user:
        new_message_text = generate_message_text(user['card']['chars'], user['card']['visibility'])
        reply_markup = get_card_keyboard()
        try:
            bot.edit_message_text(new_message_text, chat_id, message_id, parse_mode='HTML', reply_markup=reply_markup)
        except Exception as e:
            print(f"Ошибка call_command: {e}")
    else:
        print("Пользователь не найден 🚫🔍")


def generate_message_text(card_data, visibility):
    visibility_symbols = {
        "bio": " ",
        "prof": " ",
        "heal": " ",
        "phob": " ",
        "hobb": " ",
        "fact": " ",
        "bagg": " ",
        "card1": " ",
        "card2": " ",
    }

    for key in visibility:
        visibility[key] = bool(visibility[key])

    bio_data = card_data.get('bio', {})
    prof_data = card_data.get('prof', " ")
    heal_data = card_data.get('heal', " ")
    phob_data = card_data.get('phob', " ")
    hobb_data = card_data.get('hobb', " ")
    fact_data = card_data.get('fact', " ")
    bagg_data = card_data.get('bagg', " ")
    card1_data = card_data.get('card1', " ")
    card2_data = card_data.get('card2', " ")

    for key, value in visibility.items():
        if not value:
            visibility_symbols[key] = "×"

    sex = "Мужской" if bio_data.get("gender") == "М" else "Женский"

    message_text = (
        f"<b>Пол:</b> {sex}\n"
        f"{visibility_symbols['bio']} <b>БИО:</b> {bio_data.get('gender_name', '')}, "
        f"{bio_data.get('age', 0)} {bio_data.get('years', '')}, стаж работы - "
        f"{bio_data.get('age_work', 0)} {bio_data.get('years_work', '')}"
        f"{bio_data.get('fertility', '')}\n\n"
        f"{visibility_symbols['prof']} <b>Профессия:</b> {prof_data}\n"
        f"{visibility_symbols['heal']} <b>Здоровье:</b> {heal_data}\n"
        f"{visibility_symbols['phob']} <b>Фобия:</b> {phob_data}\n"
        f"{visibility_symbols['hobb']} <b>Хобби:</b> {hobb_data}\n"
        f"{visibility_symbols['fact']} <b>Факт:</b> {fact_data}\n"
        f"{visibility_symbols['bagg']} <b>Багаж:</b> {bagg_data}\n\n"
        f"{visibility_symbols['card1']} <b>Карта №1:</b> {card1_data}\n"
        f"{visibility_symbols['card2']} <b>Карта №2:</b> {card2_data}"
    )

    return message_text


def get_table_keyboard(user_id):
    keyboard = InlineKeyboardMarkup()
    admin_id = 833674307

    if int(user_id) == admin_id:
        keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="update_message"))
        keyboard.add(InlineKeyboardButton(text="Выгнать 🚪", callback_data="admin_kick_list"))
    else:
        keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="update_message"))

    return keyboard


@bot.message_handler(commands=['table'])
def table_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)

        lobby_players = database.get('lobby', {}).get('players', {})
        admin_id = 833674307

        if str(user_id) not in lobby_players and user_id != admin_id:
            bot.send_message(message.chat.id, "Вы не в игре 😕📛")
            return

        message_text = generate_table_message_text()

        for user in database['players_card']:
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

        admin_in_game = any(u['id'] == admin_id for u in database['players_card'])
        if not admin_in_game:
            kb = get_table_keyboard(admin_id)
            bot.send_message(admin_id, message_text, parse_mode='HTML', reply_markup=kb)

        save_database()
    else:
        send_subscription_message(message.chat.id)


def generate_table_message_text():
    message_text = "📋 <b>ОБЩИЙ СТОЛ</b> 📜\n"

    for user in database['players_card']:
        user_name = user['name']
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


@bot.callback_query_handler(func=lambda call: call.data == "update_message")
def update_table_message(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        message_text = generate_table_message_text()

        for user in database['players_card']:
            p_id = user['id']
            prev_msg_id = user.get('common_message_id')
            if prev_msg_id:
                with suppress(Exception):
                    bot.edit_message_text(message_text, p_id, prev_msg_id,
                                          parse_mode="HTML", reply_markup=get_table_keyboard(p_id))

        admin_id = 833674307
        admin_in_players = any(u['id'] == admin_id for u in database['players_card'])
        if user_id == admin_id and not admin_in_players:
            with suppress(Exception):
                bot.edit_message_text(message_text, admin_id, call.message.message_id,
                                      parse_mode="HTML", reply_markup=get_table_keyboard(admin_id))

        bot.answer_callback_query(call.id, "Общий стол обновлен для всех игроков! ✅")
    else:
        bot.answer_callback_query(call.id, "Чтобы обновить сообщение, подпишитесь на канал 📛", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data in ["admin_kick_list", "admin_kick_cancel"])
def handle_admin_kick_navigation(call):
    admin_id = 833674307
    if call.from_user.id != admin_id:
        return

    if call.data == "admin_kick_cancel":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=get_table_keyboard(admin_id))
        return

    keyboard = InlineKeyboardMarkup()
    for user in database['players_card']:
        if user['id'] == admin_id:
            button_text = "Себя"
        else:
            button_text = f"{user['name']}"

        keyboard.add(InlineKeyboardButton(button_text, callback_data=f"exec_kick_{user['id']}"))

    keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="admin_kick_cancel"))

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("exec_kick_"))
def handle_execute_kick(call):
    admin_id = 833674307
    if call.from_user.id != admin_id:
        return

    target_id = int(call.data.split('_')[-1])
    lobby = database['lobby']

    database['players_card'] = [p for p in database['players_card'] if p['id'] != target_id]

    player_id_str = str(target_id)
    if player_id_str in lobby['players']:
        msg_id = lobby['players'][player_id_str].get('lobby_message_id')
        if msg_id:
            with suppress(Exception):
                bot.edit_message_text("<b>Вы были удалены из игры администратором 🚫</b>",
                                      chat_id=target_id, message_id=msg_id, parse_mode='HTML')
        del lobby['players'][player_id_str]

    if not lobby['players']:
        lobby['status'] = 'CLOSED'
        save_database()
        bot.answer_callback_query(call.id, "Последний игрок удален. Игра закрыта 🔒", show_alert=True)
        bot.edit_message_text("<b>Все игроки удалены. Игра завершена 🛑</b>",
                              call.message.chat.id, call.message.message_id, parse_mode='HTML')
        return

    save_database()
    update_table_message(call)
    bot.answer_callback_query(call.id, "Игрок успешно изгнан 🗑")


@bot.message_handler(commands=['generate'])
def gen_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id != 833674307:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
            return

        lobby_players = database.get('lobby', {}).get('players', {})

        if not lobby_players:
            bot.send_message(message.chat.id, "В лобби пока никого нет 🤷‍♂️")
            return

        message_text = "🖐 Выберите игрока (-ов):"
        player_buttons = []
        for p_id in lobby_players.keys():
            p_name = database['all_users'].get(str(p_id), f"ID: {p_id}")
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

    lobby_players = database.get('lobby', {}).get('players', {})
    ids_in_game = [int(pid) for pid in lobby_players.keys()]

    if target == "all":
        for player in database['players_card']:
            if player['id'] in ids_in_game:
                update_characteristics(player, char)

        bot.edit_message_text("Характеристики сгенерированы для всех ♻", call.message.chat.id, call.message.message_id)
    else:
        player_id = int(target)
        player = next((player for player in database['players_card'] if player['id'] == player_id), None)
        if player:
            update_characteristics(player, char)
            bot.edit_message_text("Характеристика сгенерирована ♻", call.message.chat.id, call.message.message_id)
        else:
            bot.send_message(call.message.chat.id, "Игрок не найден 🚫🔍")


def update_characteristics(player, char):
    gender = player['card']['chars']['bio']['gender']

    if 'indexes' not in player['card']:
        player['card']['indexes'] = {}

    if char == "prof":
        profession, profession_index = get_profession(gender)
        player['card']['chars']['prof'] = profession
        player['card']['indexes']['prof'] = profession_index
    elif char == "heal":
        health, health_status, health_index = get_health(gender)
        player['card']['chars']['heal'] = f"{health} {health_status}"
        player['card']['indexes']['heal'] = health_index
    elif char == "phob":
        phobia, phobia_index = get_phobia()
        player['card']['chars']['phob'] = phobia
        player['card']['indexes']['phob'] = phobia_index
    elif char == "hobb":
        hobby, hobby_index = get_hobby()
        player['card']['chars']['hobb'] = hobby
        player['card']['indexes']['hobb'] = hobby_index
    elif char == "fact":
        fact, fact_index = get_fact(gender)
        player['card']['chars']['fact'] = fact
        player['card']['indexes']['fact'] = fact_index
    elif char == "bagg":
        baggage, baggage_index = get_baggage()
        player['card']['chars']['bagg'] = baggage
        player['card']['indexes']['bagg'] = baggage_index

    call_command(player['id'], player['card_message_id'])
    save_database()


@bot.message_handler(commands=['swap'])
def swap_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id != 833674307:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
            return

        lobby_players = database.get('lobby', {}).get('players', {})
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('swap_char_') or call.data == "cancel_swap")
def handle_swap_char_callback(call):
    if call.data == "cancel_swap":
        bot.edit_message_text("Вы отменили выбор ❌", call.message.chat.id, call.message.message_id)
        return

    char = call.data.split('_')[-1]
    lobby_players = database.get('lobby', {}).get('players', {})

    message_text = "1️⃣ Выберите первого игрока:"
    keyboard = []

    for player_id in lobby_players.keys():
        player_name = database['all_users'].get(str(player_id), f"ID: {player_id}")
        keyboard.append([InlineKeyboardButton(player_name, callback_data=f"select_player1_{char}_{player_id}")])

    keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id, reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_player1_'))
def handle_select_player1_callback(call):
    data = call.data.split('_')
    char, player1_id = data[2], data[3]
    lobby_players = database.get('lobby', {}).get('players', {})

    message_text = "2️⃣ Выберите второго игрока:"
    keyboard = []

    for player_id in lobby_players.keys():
        if str(player_id) == str(player1_id): continue

        player_name = database['all_users'].get(str(player_id), f"ID: {player_id}")
        keyboard.append(
            [InlineKeyboardButton(player_name, callback_data=f"select_player2_{char}_{player1_id}_{player_id}")])

    keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id, reply_markup=reply_markup,
                          parse_mode='HTML')


def get_gendered_text(array_data, item_index, gender):
    options = array_data.get(str(item_index))
    if not options:
        return "Неизвестно"

    if gender != 'М' and len(options) > 1:
        return options[1]
    return options[0]


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_player2_'))
def handle_select_player2_callback(call):
    data = call.data.split('_')
    char = data[2]
    player1_id = int(data[3])
    player2_id = int(data[4])

    player1 = next((player for player in database['players_card'] if
                    player['id'] == player1_id), None)
    player2 = next((player for player in database['players_card'] if
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

        save_database()

        call_command(player1_id, player1['card_message_id'])
        call_command(player2_id, player2['card_message_id'])

        bot.edit_message_text("Обмен харакетристик с учётом пола произведён успешно ♻",
                              call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(call.message.chat.id, "Один или оба игрока не найдены 🚫🔍")


@bot.message_handler(commands=['fertility'])
def fer_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == 833674307:
            lobby_players = database.get('lobby', {}).get('players', {})

            if not lobby_players:
                bot.send_message(message.chat.id, "В игре нет активных участников 😕📛")
                return

            message_text = "👥 Выберите игрока:"
            keyboard = []

            for player_id in lobby_players.keys():
                player_name = database['all_users'].get(str(player_id), f"ID: {player_id}")
                keyboard.append([InlineKeyboardButton(player_name, callback_data=f"remove_fertility_{player_id}")])

            keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_fertility")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение \
            этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_fertility_'))
def remove_fertility_callback(call):
    player_id = int(call.data.split('_')[-1])

    for player in database['players_card']:
        if player['id'] == player_id:
            fertility_status = player['card']['chars']['bio']['fertility']

            if ", неспособна рожать" in fertility_status or ", неспособен оплодотворять" in fertility_status:
                bot.edit_message_text("Последствия старости никак не убрать 👴🏻", call.message.chat.id,
                                      call.message.message_id)
            elif fertility_status == "":
                bot.edit_message_text("Менять нечего 🤰🏻💢", call.message.chat.id, call.message.message_id)
            else:
                player['card']['chars']['bio']['fertility'] = ""
                save_database()

                call_command(player_id, player['card_message_id'])
                bot.edit_message_text("Готово, теперь игрок плоден! 🤰🏻", call.message.chat.id, call.message.message_id)
            break


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_fertility')
def cancel_fertility_callback(call):
    bot.edit_message_text("Вы отменили выбор игрока ❌", call.message.chat.id, call.message.message_id)


@bot.message_handler(commands=['shuffle'])
def shuffle_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if user_id == 833674307:
            lobby_players = database.get('lobby', {}).get('players', {})
            ids_in_game = [int(pid) for pid in lobby_players.keys()]

            if not ids_in_game:
                bot.send_message(message.chat.id, "Нет игроков для перемешивания 🚫")
                return

            active_players = [
                player for player in database['players_card']
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

                save_database()
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
        user = next((player for player in database['players_card'] if player['id'] == user_id), None)

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

        save_database()
    else:
        send_subscription_message(message.chat.id)


nick_selection = {}
def get_profile_ui(user_id):
    user_id_str = str(user_id)
    user_name = database['all_users'].get(user_id_str, "Выживший")
    text = f"📇 <b>Профиль – {user_name}</b>\n\n📡 Ваш ID: <code>{user_id}</code>\n"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сменить никнейм ✏️", callback_data="profile_change_nick"))

    lobby = database.get('lobby', {})
    players = lobby.get('players', {})
    status = lobby.get('status', {})

    if status == "STARTED":
        text += f"🪑 <b>Статус:</b> В игре"
    elif status == "OPEN" and user_id_str in players:
        text += f"🪑 <b>Статус:</b> В лобби"
    else:
        text += "🪑 <b>Статус:</b> Вне игры"

    return text, keyboard


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
            'current_nick': database['all_users'].get(str(user_id), "Не установлен")
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

        database['all_users'][str(user_id)] = new_nick
        for player in database['players_card']:
            if player['id'] == user_id:
                player['name'] = new_nick
                break
        save_database()

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


@bot.message_handler(commands=['mikey'])
def send_circle_message(message):
    video_path = 'media/mikey.mp4'

    if os.path.exists(video_path):
        with open(video_path, 'rb') as v:
            bot.send_video_note(message.chat.id, v)
    else:
        bot.send_message(message.chat.id, "Файл видео не найден 🎥❌")


@bot.message_handler(commands=['reset'])
def reset_game_command(message):
    user_id = message.from_user.id
    admin_id = 833674307
    if user_id != admin_id:
        bot.reply_to(message, "У вас нет прав для этой команды 🔐")
        return
    database['lobby'] = {
        "status": "CLOSED",
        "players": {}
    }

    database['players_card'] = []
    database['user_ordinal'] = 1

    if 'used' in database:
        for key in database['used']:
            database['used'][key] = []
    else:
        database['used'] = {
            "professions": [],
            "healths": [],
            "phobias": [],
            "hobbies": [],
            "facts": [],
            "baggages": [],
            "cards": []
        }

    save_database()

    bot.send_message(message.chat.id, "<b>🧹 База данных успешно очищена!</b>\n\n"
                                      "• Лобби закрыто\n"
                                      "• Карты игроков удалены\n"
                                      "• Списки повторов сброшены\n\n"
                                      "Можно начинать новую игру с /play.", parse_mode='HTML')


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


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bunker_log.txt',
    filemode='a'  # 'a' значит дозаписывать в конец файла, а не стирать старое
)

bot.infinity_polling(timeout=10, long_polling_timeout=5)
