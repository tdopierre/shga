import json
from bs4 import BeautifulSoup
import requests


class VintedConfig:
    def __init__(self, urls=None):
        if urls is None:
            urls = list()
        self.urls = urls

    @classmethod
    def load_from_config_dict(cls, config_dict):
        return cls(**config_dict)

    @classmethod
    def load_from_config_path(cls, config_path):
        with open(config_path, 'r') as file:
            return cls(**(json.load(file)['vinted']))

    def __repr__(self):
        return f'<VintedConfig({", ".join([f"""{k}={v if not k.startswith("_") else "***"}""" for k, v in self.__dict__.items()])})'


class VintedHandler:
    def __init__(self, vinted_config):
        self.config = vinted_config  # type: VintedConfig

        self._session = requests.session()

    def get_items_from_url(self, url):
        response = self._session.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")
        items = soup.findAll("div", {"class": "is-visible item-box__container"})
        items = items[::-1]  # revert order to show oldest first
        for item in items:
            yield VintedItem.load_from_item_box__container(item)
        return [VintedItem.load_from_item_box__container(item) for item in soup.find_all("li", {"class": "_3DFQ-"})]

    def get_all_interesting_items(self):
        for url in self.config.urls:
            yield from self.get_items_from_url(url=url)


class VintedItem:
    def __init__(self, price, size, url, desc=None, brand=None):
        self.brand = brand
        self.price = price
        self.size = size
        self.url = url
        self.desc = desc

    @classmethod
    def load_from_item_box__container(cls, item):
        try:
            brand = item.findAll('a', {"class": "item-box__brand"})[0].text
        except:
            brand = None
        item_box_details = item.findAll("div", {"class": "item-box__details"})[0]
        price = item_box_details.findAll("div", {"class": "item-box__title"})[0].text.strip()
        size = item_box_details.findAll("div", {"class": "item-box__subtitle"})[0].text.strip()
        url = f'https://www.vinted.fr{item.findAll("a", {"class": "media__image-wrapper js-item-link"})[0].attrs["href"]}'

        return cls(brand=brand, price=price, size=size, url=url)

    def __repr__(self):
        s = ''
        if self.brand:
            s += f'Marque: {self.brand}\n'
        if self.desc:
            s += self.desc + '\n'
        if self.size:
            s += f'Taille: {self.size}\n'
        if self.price:
            s += f'Prix: {self.price}\n'
        if self.url:
            s += f'{self.url}\n'
        if s.endswith('\n'):
            s = s[:-1]
        return s

    def to_html(self):
        html = ''
        for key, val in self.__dict__.items():
            if val is not None:
                if val.startswith('http'):
                    html += f'<a href="{val}">link</a>' + '\n'
                else:
                    html += val + '\n'
        return html


config = VintedConfig.load_from_config_dict(config_dict={"urls": [
    "https://www.vinted.fr/vetements?search_text=speed%20cross&order=newest_first",
    "https://www.vinted.fr/vetements?search_text=speedcross&order=newest_first"
]})

handler = VintedHandler(config)
items = list(handler.get_items_from_url("https://www.vinted.fr/vetements?search_text=speed%20cross&order=newest_first"))
