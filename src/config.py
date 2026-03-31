import os
import telebot
from dotenv import load_dotenv
import json


load_dotenv()
CHANNEL_ID = '@bunkernewss'
ADMIN_ID = int(os.getenv('ADMIN_ID'))
bot = telebot.TeleBot(os.getenv('TELEGRAMTOKEN'))


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


professions = load_json('data/array_prof.json')
healths = load_json('data/array_heal.json')
phobias = load_json('data/array_phob.json')
hobbies = load_json('data/array_hobb.json')
facts = load_json('data/array_fact.json')
baggages = load_json('data/array_bagg.json')
cards = load_json('data/array_card.json')
