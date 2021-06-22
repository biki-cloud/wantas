import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List
import json
import os
import dataset
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import util
from scrape_server import geo
from scrape_server.geo import StoreInfo
from scrape_server.db_driver import DbDriver
from scrape_server.store.seveneleven import SevenEleven
from scrape_server.mylog import log
from scrape_server.database import database


def suited_results(result: list) -> (list):
    """
    productsテーブル用。データベースから取り出す時にjsonを整形する。
    """
    new_results = []
    for i in result:
        new_dic = {}
        for k, v in i.items():
            if k != "id":
                if k == "region_list":
                    new_dic[k] = v.split(",")
                else:
                    new_dic[k] = v
        new_results.append(new_dic)
    return new_results


def search(search_name: str, user_lat: float, user_lon: float) -> (list, float, float):
    """商品名を受け取り、スクレイプし名前が入った商品のリストを持ってくる。
    lat,lonから場所を検索し、商品が売られている場所のみをフィルターし、商品リストを返す。
    """
    log.info("invoked search function.")
    log.info(f"user lat: {user_lat}, user lon: {user_lon}")


    # get db 2
    db2 = dataset.connect("sqlite:///" + os.path.join("database", "db.sqlite"))
    product_table = db2["products"]
    result = database.search(product_table, "name", search_name)
    result = suited_results(result)


    # ユーザーから一番近い店舗の情報を取得
    store_info: StoreInfo = geo.get_most_near_store_info(user_lat, user_lon)
    log.info("got most near store information")
    log.info(store_info.__dict__)

    # ユーザーに一番近い店舗がある地域のみでフィルターする。
    filtered_results = []
    for ele in result:
        if geo.is_contains(ele['region_list'], store_info):
            filtered_results.append(ele)
    result = filtered_results

    log.info("return from search funcion.")
    log.info(f"result: {result}")
    log.info(f"most near store lat: {store_info.lat}, store lon: {store_info.lon}")
    return result, store_info.lat, store_info.lon


def main():
    db2 = dataset.connect(f"sqlite:///{os.path.join('database', 'db.sqlite')}")
    print(db2)
    product_table = db2["products"]
    print(product_table)
    # result = product_table.find(name="*カフェ*")
    result = database.search(product_table, "name", "おにぎり")
    for i in result:
        print(i)

if __name__ == '__main__':
    main()
