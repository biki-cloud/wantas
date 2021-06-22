import os, sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

import dataset

from scrape_server import util


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
    elements = util.read_json_file(json_path)
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
        if type(v) is list:
            record[k] = ",".join(record[k])
        if k == "lat" or k == "lon":
            record[k] = float(v)
        else:
            record[k] = v
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


if __name__ == '__main__':
    # init_insert_to_db("./products.json","./db.sqlite", "products")
    init_insert_to_db("./store_info.json","./db.sqlite", "store_info")

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



