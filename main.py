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


@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if str(user_id) not in database['all_users']:
        database['all_users'][str(user_id)] = user_name

        save_database()


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


@bot.message_handler(commands=['play'])
def play_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == 833674307:
            if user_id not in database['inthegame']:
                database['inthegame'].append(user_id)

            database['players_card'] = []
            database['used'] = {
                'professions': [],
                'healths': [],
                'phobias': [],
                'hobbies': [],
                'facts': [],
                'baggages': [],
                'cards': []
            }

            user_ordinal = 1

            for user_id in database['inthegame']:
                card_data = get_card()
                sent_card_message = send_generated_card(user_id, card_data)
                user_name = database['all_users'].get(str(user_id), "Unknown")
                new_user_template = {
                    "id": user_id,
                    "ordinal": user_ordinal,
                    "name": user_name,
                    "card": card_data,
                    "card_message_id": sent_card_message.message_id,
                    "common_message_id": 0
                }

                database['players_card'].append(new_user_template)
                user_ordinal += 1

            database['user_ordinal'] = user_ordinal
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")

        save_database()
    else:
        send_subscription_message(message.chat.id)


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
    chat_id = call.message.chat.id

    user = next((user for user in database['players_card'] if user['id'] == chat_id))

    if user:
        element_to_update = call.data

        user['card']['visibility'][element_to_update] = not \
            user['card']['visibility'][element_to_update]

        message_id = user['card_message_id']
        reply_markup = get_card_keyboard()

        new_message_text = generate_message_text(user['card']['chars'], user['card']['visibility'])

        bot.edit_message_text(new_message_text, chat_id, message_id, parse_mode='HTML', reply_markup=reply_markup)

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


@bot.message_handler(commands=['table'])
def table_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)

        sender_id = message.from_user.id
        admin_id = 833674307

        if sender_id != admin_id and sender_id not in database['inthegame']:
            bot.send_message(message.chat.id, "Вы не в игре 😕📛")
            return

        message_text = generate_table_message_text()
        keyboard = InlineKeyboardMarkup()
        update_button = InlineKeyboardButton(text="Обновить", callback_data="update_message")
        keyboard.add(update_button)

        for user in database['players_card']:
            user_id = user['id']
            prev_message_id = user.get('common_message_id')

            if prev_message_id:
                with suppress(Exception):
                    bot.edit_message_text(
                        message_text,
                        chat_id=user_id,
                        message_id=prev_message_id,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
            else:
                sent_message = bot.send_message(user_id, message_text, parse_mode="HTML", reply_markup=keyboard)
                user['common_message_id'] = sent_message.message_id

        admin_in_players = any(user['id'] == admin_id for user in database['players_card'])
        if not admin_in_players:
            bot.send_message(admin_id, message_text, parse_mode='HTML', reply_markup=keyboard)

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
        keyboard = InlineKeyboardMarkup()
        update_button = InlineKeyboardButton(text="Обновить", callback_data="update_message")
        keyboard.add(update_button)

        for user in database['players_card']:
            player_id = user['id']
            prev_message_id = user.get('common_message_id')

            if prev_message_id:
                with suppress(Exception):
                    bot.edit_message_text(
                        message_text,
                        chat_id=player_id,
                        message_id=prev_message_id,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )

        admin_id = 833674307
        admin_in_players = any(user['id'] == admin_id for user in database['players_card'])
        if user_id == admin_id and not admin_in_players:
            with suppress(Exception):
                bot.edit_message_text(
                    message_text,
                    chat_id=user_id,
                    message_id=call.message.message_id,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )

        bot.answer_callback_query(call.id, "Общий стол обновлен для всех игроков! ✅")

    else:
        bot.answer_callback_query(call.id, "Чтобы обновить сообщение, подпишитесь на канал 📛", show_alert=True)


@bot.message_handler(commands=['generate'])
def gen_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == 833674307:
            sender_id = message.from_user.id
            admin_id = 833674307
            if sender_id != admin_id and sender_id not in database['inthegame']:
                bot.send_message(message.chat.id, "Вы не в игре 😕📛")
                return

            message_text = "🖐 Выберите игрока (-ов):"
            player_buttons = [
                [InlineKeyboardButton(database['all_users'].get(str(p_id), "Игрок"), callback_data=f"generate_{p_id}")]
                for p_id in database['inthegame']
            ]

            keyboard = [
                [InlineKeyboardButton("Всем", callback_data="generate_all")],
                *player_buttons,
                [InlineKeyboardButton("Отменить ❌", callback_data="cancel_generate")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('generate_') or call.data == "cancel_generate")
def handle_generate_callback(call):
    if call.data == "cancel_generate":
        bot.edit_message_text("Вы отменили выбор игрока ❌", call.message.chat.id, call.message.message_id)
        return

    if call.data == "generate_all":
        chat_id = call.message.chat.id
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
        bot.edit_message_text(message_text, chat_id, call.message.message_id, reply_markup=reply_markup)
    else:
        player_id = call.data.split('_')[-1]
        chat_id = call.message.chat.id
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
        bot.edit_message_text(message_text, chat_id, call.message.message_id, reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('char_'))
def handle_char_callback(call):
    data = call.data.split('_')
    char = data[1]
    target = data[2]

    if target == "all":
        for player in database['players_card']:
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
        if message.chat.id == 833674307:
            sender_id = message.from_user.id
            admin_id = 833674307
            if sender_id != admin_id and sender_id not in database['inthegame']:
                bot.send_message(message.chat.id, "Вы не в игре 😕📛")
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
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('swap_char_') or call.data == "cancel_swap")
def handle_swap_char_callback(call):
    if call.data == "cancel_swap":
        bot.edit_message_text("Вы отменили выбор ❌", call.message.chat.id, call.message.message_id)
        return

    char = call.data.split('_')[-1]
    chat_id = call.message.chat.id
    message_text = "1️⃣ Выберите первого игрока:"
    keyboard = []

    for player_id in database['inthegame']:
        player_name = database['all_users'].get(str(player_id), "Неизвестный игрок")
        keyboard.append([InlineKeyboardButton(player_name, callback_data=f"select_player1_{char}_{player_id}")])

    keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, chat_id, call.message.message_id, reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_player1_'))
def handle_select_player1_callback(call):
    data = call.data.split('_')
    char = data[2]
    player1_id = data[3]
    chat_id = call.message.chat.id
    message_text = "2️⃣ Выберите второго игрока:"
    keyboard = []

    for player_id in database['inthegame']:
        player_name = database['all_users'].get(str(player_id), "Неизвестный игрок")
        keyboard.append([InlineKeyboardButton(player_name,
                                              callback_data=f"select_player2_{char}_{player1_id}_{player_id}")])

    keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_swap")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(message_text, chat_id, call.message.message_id, reply_markup=reply_markup)


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
    chat_id_sender = call.message.chat.id

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

        bot.edit_message_text("Харакетристики обменяты ♻", call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(chat_id_sender, "Один или оба игрока не найдены 🚫🔍")


@bot.message_handler(commands=['kick'])
def kick_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == 833674307:
            if not database['inthegame']:
                bot.send_message(message.chat.id, "В игре сейчас нет игроков 🚫")
                return

            message_text = "👤 Выберите игрока для удаления:"
            keyboard = []

            for player_id in database['inthegame']:
                player_name = database['all_users'].get(str(player_id), "Неизвестный игрок")
                keyboard.append([InlineKeyboardButton(player_name, callback_data=f"kick_player_{player_id}")])

            keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_kick")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды 🔐🚫")
    else:
        send_subscription_message(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('kick_player_') or call.data == "cancel_kick")
def handle_kick_callback(call):
    if call.data == "cancel_kick":
        bot.edit_message_text("Вы отменили выбор ❌", call.message.chat.id, call.message.message_id)
        return

    player_id = int(call.data.split('_')[-1])

    player_index = None
    for index, player in enumerate(database['players_card']):
        if player['id'] == player_id:
            player_index = index
            break

    if player_index is not None:
        del database['players_card'][player_index]

        if player_id in database['inthegame']:
            database['inthegame'].remove(player_id)

        bot.edit_message_text("Игрок успешно удалён 🗑✅", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text("Игрок не найден 🚫🔍", call.message.chat.id, call.message.message_id)

    save_database()


@bot.message_handler(commands=['id'])
def id_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        chat_id = message.chat.id
        bot.send_message(chat_id, f"🔹 Ваш id: <code>{chat_id}</code>", parse_mode='HTML')
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(commands=['fertility'])
def fer_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)
        if message.chat.id == 833674307:
            sender_id = message.from_user.id
            admin_id = 833674307
            if sender_id != admin_id and sender_id not in database['inthegame']:
                bot.send_message(message.chat.id, "Вы не в игре 😕📛")
                return

            message_text = "👥 Выберите игрока:"
            keyboard = []

            for player_id in database['inthegame']:
                player_name = database['all_users'].get(str(player_id), "Unknown")
                keyboard.append([InlineKeyboardButton(player_name, callback_data=f"remove_fertility_{player_id}")])

            keyboard.append([InlineKeyboardButton("Отменить ❌", callback_data="cancel_fertility")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(message.chat.id, message_text, reply_markup=reply_markup)

            save_database()
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
        if message.chat.id == 833674307:
            ids_in_game = database['inthegame']

            player_data = [
                {"id": player["id"], "prof_index": player["card"]["indexes"]["prof"]}
                for player in database['players_card'] if player['id'] in ids_in_game
            ]

            num_players = len(player_data)
            original_indexes = [data["prof_index"] for data in player_data]

            while True:
                shuffled_indexes = random.sample(original_indexes, num_players)
                if all(original != shuffled for original, shuffled in zip(original_indexes, shuffled_indexes)):
                    break

            for i, player_info in enumerate(player_data):
                new_prof_index = shuffled_indexes[i]
                player_id = player_info["id"]

                player = next((p for p in database['players_card'] if p['id'] == player_id), None)
                if player:
                    gender = player["card"]["chars"]["bio"]["gender"]
                    if gender == 'М':
                        new_prof = professions[str(new_prof_index)][0]
                    else:
                        if len(professions[str(new_prof_index)]) > 1:
                            new_prof = professions[str(new_prof_index)][1]
                        else:
                            new_prof = professions[str(new_prof_index)][0]

                    player["card"]["indexes"]["prof"] = new_prof_index
                    player["card"]["chars"]["prof"] = new_prof

            save_database()

            for player in database['players_card']:
                if player['id'] in ids_in_game:
                    try:
                        call_command(player['id'], player['card_message_id'])
                    except Exception as e:
                        bot.send_message(message.chat.id,
                                         f"Ошибка при обновлении карточки игрока {player['name']}: {str(e)} ⚠")

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


@bot.message_handler(commands=['setnick'])
def set_nick_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        with suppress(Exception):
            bot.delete_message(message.chat.id, message.message_id)

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="setnick_cancel_initial"))

        sent_message = bot.send_message(
            message.chat.id,
            "💁‍♀️ Укажите свой новый никнейм:",
            reply_markup=keyboard
        )

        nick_selection[user_id] = {
            'stage': 'awaiting_nick',
            'message_id': sent_message.message_id,
            'current_nick': database['all_users'].get(str(user_id), "Не установлен")
        }
    else:
        send_subscription_message(message.chat.id)


@bot.message_handler(func=lambda msg: nick_selection.get(msg.from_user.id, {}).get('stage') == 'awaiting_nick')
def receive_nick(message):
    user_id = message.from_user.id
    new_nick = message.text

    bot.delete_message(message.chat.id, message.message_id)

    user_data = nick_selection.get(user_id)
    if not user_data:
        return

    nick_selection[user_id]['nick'] = new_nick
    nick_selection[user_id]['stage'] = 'confirming'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сменить ✅", callback_data="setnick_confirm"))
    keyboard.add(InlineKeyboardButton("Редактировать 📝", callback_data="setnick_edit"))
    keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="setnick_cancel"))

    current_nick = user_data.get('current_nick', "Не установлен")
    bot.edit_message_text(
        f"💁‍♀️ Сменить ваш текущий никнейм <b>\"{current_nick}\"</b> на новый <b>"
        f"\"{new_nick}\"</b>?\n\nПодтвердите действие:",
        message.chat.id,
        user_data['message_id'],
        reply_markup=keyboard,
        parse_mode='HTML'
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("setnick_"))
def handle_nick_confirmation(call):
    user_id = call.from_user.id
    user_data = nick_selection.get(user_id)

    if not user_data:
        bot.answer_callback_query(call.id, "Ошибка: не найдено активное изменение ника")
        return

    action = call.data.split("_")[1]

    if action == "cancel_initial":
        nick_selection.pop(user_id, None)

        bot.edit_message_text(
            "Вы отменили смену никнейма ❌",
            call.message.chat.id, call.message.message_id
        )
        return

    if action == "confirm":
        new_nick = user_data['nick']

        database['all_users'][str(user_id)] = new_nick

        for player in database['players_card']:
            if player['id'] == user_id:
                player['name'] = new_nick
                break

        save_database()

        bot.edit_message_text(
            f'Ваш новый никнейм <b>"{new_nick}"</b> успешно установлен ✅',
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        nick_selection.pop(user_id, None)

    elif action == "edit":
        nick_selection[user_id]['stage'] = 'awaiting_nick'

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Отменить ❌", callback_data="setnick_cancel_initial"))

        bot.edit_message_text(
            "💁‍♀️ Укажите свой новый никнейм:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif action == "cancel":
        bot.edit_message_text(
            "Вы отменили смену никнейма ❌",
            call.message.chat.id,
            call.message.message_id
        )
        nick_selection.pop(user_id, None)


def send_subscription_message(chat_id):
    keyboard = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}")
    keyboard.add(subscribe_button)
    bot.send_message(
        chat_id,
        "Чтобы пользоваться этим ботом, вы должны быть подписаны на новостной канал! 😄👇",
        reply_markup=keyboard
    )


@bot.message_handler(commands=['mikey'])
def send_circle_message(message):
    video_path = 'media/mikey.mp4'

    if os.path.exists(video_path):
        with open(video_path, 'rb') as v:
            bot.send_video_note(message.chat.id, v)
    else:
        bot.send_message(message.chat.id, "Файл видео не найден 🎥❌")


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
