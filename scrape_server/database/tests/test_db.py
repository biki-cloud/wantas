import os
from typing import List

import dataset

from scrape_server import util
from scrape_server.database import db


def get_product_info_dict_list() -> (List[dict]):
    return [
        {
            "product_name": "手巻おにぎり　炙り焼さば",
            "product_url": "https://www.sej.co.jp/products/a/item/045687/hokkaido",
            "product_price": "125円（税込135円）",
            "product_region_list": [
                "北海道"
            ],
            "product_img_url": "https://img.7api-01.dp1.sej.co.jp/item-image/045687/D10E5252B4B52AA7139ECAE5D7DFFBB3.jpg",
            "store_table_name": "store_seveneleven"
        },
        {
            "product_name": "北海道米こだわりおむすび　道産帆立山わさび添え",
            "product_url": "https://www.sej.co.jp/products/a/item/045680/hokkaido",
            "product_price": "160円（税込172.80円）",
            "product_region_list": [
                "北海道"
            ],
            "product_img_url": "https://img.7api-01.dp1.sej.co.jp/item-image/045680/D9C54C8C5981CA17BBA6C99E44B0AF78.jpg",
            "store_table_name": "store_seveneleven"
        }]


def get_store_info_dic_list() -> (List[dict]):
    return [{
        "store_name": "ローソン赤平幌岡店",
        "store_address": "北海道赤平市幌岡町５４",
        "store_lat": "43.579571",
        "store_lon": "142.037059"
    },
        {
            "store_name": "ローソン旭川８条十丁目店",
            "store_address": "北海道旭川市８条通１０−２１９１−６",
            "store_lat": "43.772961",
            "store_lon": "142.367272"
        }]


def get_test_sqlite(tmp_path):
    test_dir_path = os.path.join(tmp_path, "sub")
    d = tmp_path / "sub"
    d.mkdir()
    db_path = os.path.join(f"{tmp_path}/sub", "test.sqlite")
    database = dataset.connect()

    return database


def test_JsonDbDriver(tmp_path):
    # pytestが自動でディレクトリを作成
    d = tmp_path / "sub"
    d.mkdir()
    database_file_path = d / "db.json"
    db_driver = db.JsonDbDriver(database_file_path)
    li = [
        {
            "name": "biki"
        },
        {
            "age": 22
        }
    ]
    db_driver.put(li)
    assert db_driver.get_all() == li
    li2 = [
        {
            "area": "tohoku"
        },
        {
            "class name": "mage"
        }
    ]
    db_driver.put(li2)
    li.extend(li2)
    assert db_driver.get_all() == li


def test_json_to_db(tmp_path):
    test_dir_path = tmp_path / "test"
    d = test_dir_path
    d.mkdir()
    assert True == os.path.exists(test_dir_path)

    product_dic_list = get_product_info_dict_list()
    # JSONファイルを作成
    json_file_path = os.path.join(test_dir_path, "test.json")
    util.write_json_file(json_file_path, product_dic_list)
    assert True == os.path.exists(json_file_path)

    db_path = os.path.join(test_dir_path, "test.sqlite")
    database = dataset.connect(f"sqlite:///{db_path}")
    table_name = "test_table"

    # jsonの内容をdatabaseに入れる
    db.json_to_db(json_file_path, db_path, table_name)

    # データが入っているか確認, イテレータを返す
    table = database[table_name]
    assert len(product_dic_list) == len(table)
    for i, ele in enumerate(table):
        # ele is orderedDict
        assert product_dic_list[i]['product_name'] == ele['product_name']
        assert product_dic_list[i]['store_table_name'] == ele['store_table_name']


def test_is_contains(tmp_path):
    database = get_test_sqlite(tmp_path)
    table_name = "test_table"

    table = database.get_table(table_name)
    test_dict_list = get_product_info_dict_list()
    for ele in test_dict_list:
        ele['product_region_list'] = "".join(ele['product_region_list'])
        table.insert(ele)
        assert True == db.is_contains(table, ele)
    test_dic = {
        "name": "mike",
        "age": 22
    }
    assert False == db.is_contains(table, test_dic)


def test_to_suited_dict():
    # dict -> database
    test_dic = {
        "store_name": "ローソン赤平幌岡店",
        "store_address": "北海道赤平市幌岡町５４",
        "store_lat": "43.579571",
        "store_lon": "142.037059"
    }
    collect_dic = {
        "store_name": "ローソン赤平幌岡店",
        "store_address": "北海道赤平市幌岡町５４",
        "store_lat": 43.579571,
        "store_lon": 142.037059
    }
    assert collect_dic == db.to_suited_dict(test_dic)


def test_insert(tmp_path):
    database = get_test_sqlite(tmp_path)
    products_table = database['products']
    product_info_dict_list = get_product_info_dict_list()
    for dic in product_info_dict_list:
        suited_dict = db.to_suited_dict(dic)
        products_table.insert(suited_dict)
        db.insert(products_table, dic)
    assert len(product_info_dict_list) == len(products_table)

    stores_table = database['stores']
    store_info_dict_list = get_store_info_dic_list()
    for dic in store_info_dict_list:
        suited_dict = db.to_suited_dict(dic)
        stores_table.insert(suited_dict)
        db.insert(stores_table, dic)
    assert len(store_info_dict_list) == len(stores_table)


def test_search(tmp_path):
    database = get_test_sqlite(tmp_path)
    table = database['test_table']
    assert 0 == len(table)
    product_info_dic_list = get_product_info_dict_list()
    for dic in product_info_dic_list:
        db.insert(table, dic)

    results = db.search(table, "product_name", "手巻おにぎり　炙り焼さば")
    assert 1 == len(results)

    try:
        results = db.search(table, "aname", "mike")
    except BaseException as e:
        assert "doesn't contain" in str(e)


def test_suited_products_table(tmp_path):
    database = get_test_sqlite(tmp_path)
    table = database['test_table']
    assert 0 == len(table)
    product_info_dic_list = get_product_info_dict_list()
    for dic in product_info_dic_list:
        db.insert(table, dic)

    results = db.search(table, "product_name", "手巻おにぎり　炙り焼さば")
    suited_results = db.suited_products_table(results)
    for ele in suited_results:
        assert product_info_dic_list[0] == ele


def test_suited_store_table(tmp_path):
    database = get_test_sqlite(tmp_path)
    table = database['store_table']
    assert 0 == len(table)
    test_dic = {
        "store_name": "ローソン赤平幌岡店",
        "store_address": "北海道赤平市幌岡町５４",
        "store_lat": "43.579571",
        "store_lon": "142.037059"
    }
    collect_dic = {
        "store_name": "ローソン赤平幌岡店",
        "store_address": "北海道赤平市幌岡町５４",
        "store_lat": 43.579571,
        "store_lon": 142.037059
    }

    db.insert(table, test_dic)
    results_gene = db.suited_store_table(table)
    for i in results_gene:
        assert i == collect_dic
        return
