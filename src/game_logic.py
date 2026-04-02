import random
from contextlib import suppress
from src.database_mgr import db_manager
from src.config import professions, healths, phobias, baggages, hobbies, facts, cards
from src.config import bot
from src.utils import get_years, get_years_work,  generate_message_text
from src.ui_utils import get_lobby_ui, get_card_keyboard

def get_profession(gender):
    used_professions = db_manager.data['used']['professions']

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
    used_healths = db_manager.data['used']['healths']

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
    used_phobias = db_manager.data['used']['phobias']

    while True:
        phobia_index = random.choice(list(phobias.keys()))
        if phobia_index not in used_phobias:
            phobia = phobias[phobia_index][0]
            used_phobias.append(phobia_index)
            break

    return phobia, phobia_index


def get_hobby():
    used_hobbies = db_manager.data['used']['hobbies']

    while True:
        hobby_index = random.choice(list(hobbies.keys()))
        if hobby_index not in used_hobbies:
            hobby = hobbies[hobby_index][0]
            used_hobbies.append(hobby_index)
            break

    return hobby, hobby_index


def get_fact(gender):
    used_facts = db_manager.data['used']['facts']

    while True:
        fact_index = random.choice(list(facts.keys()))
        if fact_index not in used_facts:
            fact = facts[fact_index][0] if gender == "М" else facts[fact_index][1]
            used_facts.append(fact_index)
            return fact, fact_index


def get_baggage():
    used_baggages = db_manager.data['used']['baggages']
    selected_items = []
    selected_indexes = []

    count = 2 if random.random() <= 0.9 else 1

    while len(selected_items) < count:
        baggage_index = random.choice(list(baggages.keys()))
        if baggage_index not in used_baggages and baggage_index not in selected_indexes:
            selected_items.append(baggages[baggage_index][0])
            selected_indexes.append(baggage_index)
            used_baggages.append(baggage_index)

    if len(selected_items) == 2:
        item1 = selected_items[0]
        item2 = selected_items[1]
        item2_lower = item2[0].lower() + item2[1:]
        baggage_str = f"{item1} и {item2_lower}"
    else:
        baggage_str = selected_items[0]

    return baggage_str, ", ".join(selected_indexes)


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

    used_cards = db_manager.data['used']['cards']

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

    db_manager.data['used']['cards'].extend([card1_index, card2_index])

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
    db_manager.save()


def broadcast_lobby_update():
    for pid, pdata in db_manager.data['lobby']['players'].items():
        msg_id = pdata.get('lobby_message_id')
        if msg_id:
            text, kb = get_lobby_ui(pid)
            with suppress(Exception):
                bot.edit_message_text(text, chat_id=int(pid), message_id=msg_id, reply_markup=kb, parse_mode='HTML')


def call_command(chat_id, message_id):
    user = next((user for user in db_manager.data['players_card'] if user['card_message_id'] == message_id), None)

    if user:
        new_message_text = generate_message_text(user['card']['chars'], user['card']['visibility'])
        reply_markup = get_card_keyboard()
        try:
            bot.edit_message_text(new_message_text, chat_id, message_id, parse_mode='HTML', reply_markup=reply_markup)
        except Exception as e:
            print(f"Ошибка call_command: {e}")
    else:
        print("Пользователь не найден 🚫🔍")
