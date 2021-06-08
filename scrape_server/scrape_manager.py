import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List
import json
import os
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import util
from scrape_server import geo
from scrape_server.db_driver import DbDriver
from scrape_server.store.seveneleven import SevenEleven


def search(search_name: str, user_lat: float, user_lon: float) -> (list, float, float):
    """商品名を受け取り、スクレイプし名前が入った商品のリストを持ってくる。
    lat,lonから場所を検索し、商品が売られている場所のみをフィルターし、商品リストを返す。
    """

    seven = SevenEleven()

    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")
    db_driver = DbDriver(database_path)

    elements = db_driver.get_all()

    result = db_driver.search(search_name)

    store_lat, store_lon = geo.get_store_lat_lon(user_lat, user_lon)

    filtered_results = []
    for ele in result:
        for place in ele['region_list']:
            if geo.is_here(place, user_lat, user_lon):
                filtered_results.append(ele)


    print("***** result *****")
    print(f"total: {len(elements)}")
    print(f"hits:  {len(result)}")
    print("******************")
    return filtered_results, store_lat, store_lon



def main():
    result, store_lat, store_lon = search("ご飯", 143.3, 24.2)
    print("result")
    print(result)
    print(f"store_lat: {store_lat}")
    print(f"store_lot: {store_lon}")


if __name__ == '__main__':
    main()
