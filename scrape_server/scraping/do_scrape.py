import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import sys

from scraping.seveneleven import search
from scraping.scrape_util import *

def instead_scrape(name: str) -> (str, int):
    store_list = ["seven eleven", "family mart", "yamazaki", "mini stop", "lawson"]
    store = store_list[random.randint(0, len(store_list) - 1)]
    price = random.randint(100, 1000)
    return store, price


def scrape_seven(search_name):
    return search(search_name)


def main():
    # instead_scrape("fami tiki")
    result = search("チキン")
    print(dict_to_json(result))
    print(len(result))


if __name__ == '__main__':
    main()
