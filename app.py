import telegram
from util import AppConfig
from util import CacheHandler
from util.lbc import LBCConfig, LBCHandler
from util.vinted import VintedConfig, VintedHandler

# Load globals
config_path = 'config.json'
config = AppConfig.load_from_disk(config_path)
bot = telegram.Bot(token=config.telegram_token)
cache_handler = CacheHandler()


def process_vinted():
    vinted_config = VintedConfig.load_from_config_path(config_path)
    vinted_handler = VintedHandler(vinted_config)
    for item in vinted_handler.get_all_interesting_items():
        if item.url in cache_handler:
            continue
        cache_handler.add(item.url)
        bot.send_message(chat_id=config.telegram_chat_id,
                         text=str(item),
                         parse_mode=telegram.ParseMode.HTML)
        cache_handler.save()


def process_lbc():
    lbc_config = LBCConfig.load_from_config_path(config_path)
    lbc_handler = LBCHandler(lbc_config)
    for item in lbc_handler.get_all_interesting_items():
        if item.url in cache_handler:
            continue
        cache_handler.add(item.url)
        bot.send_message(chat_id=config.telegram_chat_id,
                         text=str(item),
                         parse_mode=telegram.ParseMode.HTML)
        cache_handler.save()


def main():
    process_vinted()
    process_lbc()


if __name__ == "__main__":
    main()
