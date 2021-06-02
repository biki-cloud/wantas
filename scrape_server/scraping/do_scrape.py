import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import sys
from seveneleven import SevenEleven

def instead_scrape(name: str) -> (str, int):
    store_list = ["seven eleven", "family mart", "yamazaki", "mini stop", "lawson"]
    store = store_list[random.randint(0, len(store_list) - 1)]
    price = random.randint(100, 1000)
    return store, price


def main():
    instead_scrape("fami tiki")


if __name__ == '__main__':
    main()
