import os, sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

import dataset
from typing import List
import requests

from scrape_server.util import *
from scrape_server.store import AbsStore
from scrape_server.store.seveneleven import SevenEleven


class DatabasePathIsNotExistsError(Exception):
    pass


class TableNameIsNotExistsError(Exception):
    pass


def init_insert_to_db(json_path: str, database_path: str, table_name: str):
    """
    database_path: なければデータベースを作成
    table_name: なければテーブルを作成
    json_path: jsonを読み込んで中身をテーブルに入れる。
    """
    elements = read_json_file(json_path)
    # データベースに接続(なければ自動的に作成)
    db = dataset.connect(f"sqlite:///{database_path}")

    table = db[table_name]

    for element_dic in elements:
        insert(table, element_dic)

    # table.delete()
def is_contains(table: dataset.table.Table, record: dict) -> (bool):
    """
    recordがtableに含まれているか
    """
    all_element = table.find()
    for ordered_dic in all_element:
        new_dic_from_ordered_dic = {}
        for k, v in ordered_dic.items():
            if k != "id":
                new_dic_from_ordered_dic[k] = v
        if new_dic_from_ordered_dic == record:
            return True
    return False

def to_suited_dict(record: dict) -> (dict):
    """
    バリューがリストの場合はデータベースに入らないのでコンマでセパレートした文字列に変換する
    element -> database
    """
    for k, v in record.items():
        if k == "region_list":
            record[k] = ",".join(v)
        elif k == "lat" or k == "lon":
            record[k] = float(v)
        else:
            record[k] = str(v)
    return record

def insert(table: dataset.table.Table, record: dict):
    """recordがテーブルの中に存在しない場合のみinsertを行う"""
    suited_record = to_suited_dict(record)
    if is_contains(table, suited_record) is False:
        table.insert(record)

def search(table: dataset.table.Table, key: str, name: str):
    results = []
    all_ele = table.find()
    for ele in all_ele:
        if key not in ele.keys():
            raise BaseException(f"{key} doesn't contain in {ele}")
        if name in ele[key]:
            results.append(ele)
    return results

def suited_products_table(result: list) -> (list):
    """
    productsテーブル用。データベースから取り出す時にjsonを整形する。
    """
    def suited(d: dict) -> (dict):
        new = {}
        for k, v in d.items():
            if k != "id":
                if k == "region_list":
                    new[k] = v.split(",")
                else:
                    new[k] = v
        return new
    return [suited(d) for d in result]

def suited_store_table(table: dataset.table.Table):
    """
    store_infoテーブル用。全てのレコードを取り出し、lat,lonをfloatにした要素を含むdictのリストを返す。
    """
    def suited(d: dict) -> (dict):
        new = {}
        for k, v in d.items():
            if k != "id":
                if k == "lat" or k == "lon":
                    new[k] = float(v)
                else:
                    new[k] = v
        return new
    return [suited(d) for d in table.find()]

def seveneleven_to_db(db_path: str):
    """セブンイレブンの全商品をスクレイピングで取得し、databaseのproductsテーブルに入れる。

    Args:
        db_path (str): データベースのパス
    """
    seven = SevenEleven()
    # スクレイピング
    results = seven.get_all_product()
    print(f"all_length: {len(results)}")

    # DBへ登録
    db = dataset.connect(f"sqlite:///{db_path}")
    table = db["products"]
    for element_dic in results:
        insert(table, element_dic)

def delete_table(db_path: str, table_name: str):
    db = dataset.connect(f"sqlite:///{db_path}")
    table = db[table_name]
    table.delete()

class JsonDbDriver:
    """
    jsonに対し、データの書き込み、読み込みを行うクラス。データベースの簡易版。
    """
    def __init__(self, database_path):
        self.database_path = database_path

    def put(self, data: List[dict]):
        if os.path.exists(self.database_path):
            elements = self.get_all()
        else:
            elements = []
        for d in data:
            if d not in elements:
                elements.append(d)
        write_json_file(self.database_path, elements)

    def search(self, search_name) -> (List[dict]):
        results = []
        for record in self.get_all():
            if search_name in record['name']:
                results.append(record)
        return results

    def scrape_and_put(self, store: AbsStore):
        elements = store.get_all_product()
        self.put(elements)

    def get_all(self) -> (List[dict]):
        return read_json_file(self.database_path)

if __name__ == '__main__':
    # init_insert_to_db("./products.json","./db.sqlite", "products")
    # init_insert_to_db("./store_info.json","./db.sqlite", "store_info")
    seveneleven_to_db("./db.sqlite")
    # delete_table("./db.sqlite", "products")

# # "address"テーブルを開く(なければ自動的に作成)
# address = db["address"]

# # レコードの追加(dictのキーによって自動的にフィールドが追加される)
# address.insert({"name":"aaa", "address": "an address"})
# address.insert({"name":"bbb", "address": "some address"})
# address.insert({"name":"ccc", "address": "any address"})


# # "aaa"さんのレコードを取り出す
# # findは当てはまったレコードを全て取得。
# aaa = address.find_one(name="aaa")
# print(type(aaa))
# print(aaa.get("address")) # an address
# print(aaa.get("nothing")) # None

# data = address.find()
# print(type(data))
# for i in data:
#     print(i) # OrderedDict
#     print(i.get("address")) # print address
#     print(i.get("nothing")) # print None

# address.delete()


