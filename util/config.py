import json


class AppConfig:
    def __init__(self, telegram_token, telegram_chat_id):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    @classmethod
    def load_from_disk(cls, path):
        with open(path, 'r') as file:
            config = json.load(file)
        return cls(
            telegram_token=config.get("telegram_token"),
            telegram_chat_id=config.get("telegram_chat_id"),
        )
