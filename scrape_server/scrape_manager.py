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
from scrape_server.geo import StoreInfo
from scrape_server.db_driver import DbDriver
from scrape_server.store.seveneleven import SevenEleven


def search(search_name: str, user_lat: float, user_lon: float) -> (list, float, float):
    """商品名を受け取り、スクレイプし名前が入った商品のリストを持ってくる。
    lat,lonから場所を検索し、商品が売られている場所のみをフィルターし、商品リストを返す。
    """
    print("invoked search of scrape_manager.py")
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")
    db = DbDriver(db_path)

    result = db.search(search_name)

    # ユーザーから一番近い店舗の情報を取得
    store_info: StoreInfo = geo.get_shortest_store_info(user_lat, user_lon)
    print("got store information")
    print(store_info.__dict__)

    # ユーザーに一番近い店舗がある地域のみでフィルターする。
    filtered_results = []
    for ele in result:
        if geo.is_contains(ele['region_list'], store_info):
            filtered_results.append(ele)
    result = filtered_results

    return result, store_info.lat, store_info.lon


def main():
    # lat, lonをランダムにしよう
    result, store_lat, store_lon = search("おむすび", 43.242, 143.44)
    print(f"store_lat: {store_lat}")
    print(f"store_lot: {store_lon}")
    for i in result:
        print(util.dict_to_json(i))


if __name__ == '__main__':
    main()
