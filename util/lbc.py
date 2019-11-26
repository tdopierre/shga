import re
from util.util import clean_txt
from bs4 import BeautifulSoup
import json
import requests


class LBCConfig:
    def __init__(self, urls=None, login=None, password=None, use_saved_searches=False):
        if urls is None:
            urls = list()
        self.urls = urls
        self.login = login
        self._password = password
        self.use_saved_searches = use_saved_searches

    @classmethod
    def load_from_config_dict(cls, config_dict):
        return cls(**config_dict)

    @classmethod
    def load_from_config_path(cls, config_path):
        with open(config_path, 'r') as file:
            return cls(**(json.load(file)['lbc']))

    def __repr__(self):
        return f'<LBCConfig({", ".join([f"""{k}={v if not k.startswith("_") else "***"}""" for k, v in self.__dict__.items()])})'


class LBCHandler:
    def __init__(self, lbc_config: LBCConfig):
        self.config = lbc_config  # type: LBCConfig
        self._session = requests.session()
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.leboncoin.fr/',
            'Content-Type': 'application/json',
            'Origin': 'https://www.leboncoin.fr',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        if self.config.login and self.config._password and self.config.use_saved_searches:
            self._login()

    def _login(self):
        data = {
            'client_id': 'frontweb',
            'grant_type': 'password',
            'password': self.config._password,
            'username': self.config.login
        }
        response = self._session.post('https://api.leboncoin.fr/api/oauth/v1/token', data=data)
        bearer = json.loads(response.text)["access_token"]
        self._headers['Authorization'] = f'Bearer {bearer}'

    def get_saved_searches(self):
        return json.loads(self._session.get('https://api.leboncoin.fr/api/mysearch/v1/searches', headers=self._headers).text)

    def get_items_from_query_search(self, query):
        if "limit" not in query:
            query["limit"] = 25
        if "limit_alu" not in query:
            query["limit_alu"] = 1

        results = json.loads(self._session.post('https://api.leboncoin.fr/finder/search', headers=self._headers, data=json.dumps(query)).text)['ads']
        return [LBCItem.load_from_lbc_api(item) for item in results]

    def get_items_from_url(self, url):
        r = self._session.get(url, headers=self._headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [LBCItem.load_from_search_page(item) for item in soup.find_all("li", {"class": "_3DFQ-"})]

    def get_all_interesting_items(self):
        for saved_search in self.get_saved_searches():
            yield from self.get_items_from_query_search(query=saved_search['query'])
        for url in self.config.urls:
            yield from self.get_items_from_url(url=url)


class LBCItem:
    def __init__(self,
                 title=None,
                 price=None,
                 url=None,
                 location=None,
                 first_publication_date=None,
                 category=None,
                 description=None,
                 attributes=None,
                 images=None):

        self.title = title
        self.price = price
        self.url = url
        self.location = location
        self.first_publication_date = first_publication_date
        self.category = category
        self.description = description
        self.attributes = attributes
        self.images = images

    def __repr__(self):
        s = ''
        if self.title:
            s += self.title + '\n'
        if self.price:
            s += f'Prix: {str(self.price)}€' + '\n'
        if self.attributes:
            for d in self.attributes:
                if d['generic']:
                    s += f'{d["key_label"]}: {d["value_label"]}' + '\n'
        if self.location:
            s += self.location + '\n'
        # if self.description:
        #     if len(self.description) > 200:
        #         shortened = True
        #     else:
        #         shortened = False
        #     desc_short = self.description[:200]
        #     if shortened:
        #         desc_short += '...'
        #     desc_short += '\n'
        #     s += desc_short
        if self.url:
            s += self.url + '\n'
        if s[-1] == '\n':
            s = s[:-1]
        return s

    @classmethod
    def load_from_lbc_api(cls, item):
        try:
            location = item['location']
            location_list = list()
            if 'city_label' in location:
                location_list.append(location['city_label'])
            if 'department_name' in location:
                location_list.append(location['department_name'])
            if 'region_name' in location:
                location_list.append(location['region_name'])
            location_str = ' / '.join(location_list)
        except:
            location_str = None

        return cls(
            title=item.get('subject'),
            price=item.get('price', [None])[0],
            url=item.get('url'),
            location=location_str,
            first_publication_date=item.get("first_publication_date"),
            category=item.get("category_name"),
            description=item.get("body"),
            attributes=item.get("attributes"),
            images=item.get("images")
        )

    @classmethod
    def load_from_search_page(cls, soup_item):
        title = clean_txt(soup_item.find_all("span", {"itemprop": "name"})[0].text)
        try:
            price = clean_txt(soup_item.find_all("span", {"itemprop": "priceCurrency"})[0].text)
            price = re.sub(r'[\s€]', '', price)
        except:
            price = None
        url = 'https://www.leboncoin.fr' + soup_item.find_all("a", {"class": "clearfix trackable"})[0].attrs['href']

        return cls(
            price=price, title=title, url=url
        )
