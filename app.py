import telegram
from util import AppConfig, CacheHandler, get_vinted_items_from_url, get_lbc_items_from_url

# Load globals
config = AppConfig.load_from_disk('config.json')
bot = telegram.Bot(token=config.telegram_token)
cache_handler = CacheHandler()


def process_vinted_urls():
    for url in config.vinted_urls:

        vinted_items = get_vinted_items_from_url(url)

        for vinted_item in vinted_items:
            # print(vinted_item.to_html())
            if vinted_item.url in cache_handler:
                continue
            cache_handler.add(vinted_item.url)
            bot.send_message(chat_id=config.telegram_chat_id,
                             text=vinted_item.to_html(),
                             parse_mode=telegram.ParseMode.HTML)
            cache_handler.save()


def process_lbc_urls():
    for url in config.lbc_urls:

        lbc_items = get_lbc_items_from_url(url)

        for item in lbc_items:
            # print(vinted_item.to_html())
            if item.url in cache_handler:
                continue
            cache_handler.add(item.url)
            bot.send_message(chat_id=config.telegram_chat_id,
                             text=item.to_html(),
                             parse_mode=telegram.ParseMode.HTML)
            cache_handler.save()


def main():
    process_vinted_urls()
    process_lbc_urls()


if __name__ == "__main__":
    main()
