import os
import re


def clean_txt(txt):
    txt = re.sub(r'\u200b', r'', txt)
    txt = re.sub(r'[\s]+', ' ', txt)
    return txt.strip()


class CacheHandler:
    def __init__(self, path=os.path.join(os.environ["HOME"], '.cache', 'shga.cache')):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        if os.path.exists(path):
            with open(path, 'r') as file:
                self.items = [str(line.strip()) for line in file.readlines()]
        else:
            self.items = list()

    def save(self):
        with open(self.path, 'w') as file:
            for item in self.items:
                file.write(item + '\n')

    def add(self, item):
        self.items.append(str(item))

    def __contains__(self, item):
        return item in self.items
