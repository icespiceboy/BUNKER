import json

class DatabaseManager:
    def __init__(self, filename='database.json'):
        self.filename = filename
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"lobby": {"status": "CLOSED", "players": {}}, "all_users": {}, "players_card": []}

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

db_manager = DatabaseManager()