import os, sys
sys.path.append("/Users/hibiki/Desktop/go/wants")
sys.path.append("/code")

import dataset
from typing import List
import requests

from scrape_server.util import *
from scrape_server.store import AbsStore
from scrape_server.store.seveneleven import SevenEleven
from scrape_server.store.familymart import FamilyMart


class DatabasePathIsNotExistsError(Exception):
    pass


class TableNameIsNotExistsError(Exception):
    pass


def json_to_db(json_path: str, database_path: str, table_name: str):
    """JSONファイルの中身をDBに登録する。
    呼び出し方
    init_insert_to_db("./product_seven.json","./db.sqlite", "products")

    Args:
        json_path (str): jsonを読み込んで中身をテーブルに入れる。
        database_path (str): なければデータベースを作成
        table_name (str): なければテーブルを作成
    """
    elements = read_json_file(json_path)

    # データベースに接続(なければ自動的に作成)
    db = dataset.connect(f"sqlite:///{database_path}")

    table = db[table_name]

    for element_dic in elements:
        insert(table, element_dic)

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
        if k == "product_region_list":
            record[k] = ",".join(v)
        elif k == "store_lat" or k == "store_lon":
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
                if k == "product_region_list":
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
                if k == "store_lat" or k == "store_lon":
                    new[k] = float(v)
                else:
                    new[k] = v
        return new
    return [suited(d) for d in table.find()]

def store_to_db(db_path: str, table_name: str, store: AbsStore):
    """セブンイレブンの全商品をスクレイピングで取得し、databaseのproductsテーブルに入れる。
    呼び出し方
    seven = SevenEleven()
    store_to_db("./db.sqlite", seven)

    Args:
        db_path (str): データベースのパス
        store (AbsStore): sevenelevenやfamilymartクラスの親クラス、
            必ずget_all_product()メソッドを持っている。
    """
    # スクレイピング
    results = store.get_all_product()
    print(f"all_length: {len(results)}")

    # DBへ登録
    db = dataset.connect(f"sqlite:///{db_path}")
    table = db[table_name]
    for element_dic in results:
        insert(table, element_dic)

def delete_table(db_path: str, table_name: str):
    """テーブルを削除する
    呼び出し方
    delete_table("./db.sqlite", "products")

    Args:
        db_path (str): DBのパス
        table_name (str): テーブルの名前
    """
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

def recreate_sqlite_db(db_path: str):
    json_to_db("./product_familymart.json", db_path, "products")
    json_to_db("./product_seveneleven.json", db_path, "products")
    json_to_db("./store_seveneleven.json", db_path, "store_seveneleven")
    json_to_db("./store_familymart.json", db_path, "store_familymart")

if __name__ == '__main__':
    recreate_sqlite_db("./db.sqlite")