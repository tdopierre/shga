import telegram
from util import AppConfig, CacheHandler, get_vinted_items_from_url

config = AppConfig.load_from_disk('config.json')
bot = telegram.Bot(token=config.telegram_token)
cache_handler = CacheHandler()

for url in config.vinted_urls:

    vinted_items = get_vinted_items_from_url(url)

    for vinted_item in vinted_items:
        # print(vinted_item.to_html())
        if vinted_item.product_url in cache_handler:
            continue
        cache_handler.add(vinted_item.product_url)
        bot.send_message(chat_id=config.telegram_chat_id,
                         text=vinted_item.to_html(),
                         parse_mode=telegram.ParseMode.HTML)
        cache_handler.save()
