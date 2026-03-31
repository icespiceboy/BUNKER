from src.config import bot, CHANNEL_ID

def check_subscription(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка check_subscription: {e}")
        return False


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


def get_gendered_text(array_data, item_index, gender):
    options = array_data.get(str(item_index))
    if not options:
        return "Неизвестно"

    if gender != 'М' and len(options) > 1:
        return options[1]
    return options[0]
