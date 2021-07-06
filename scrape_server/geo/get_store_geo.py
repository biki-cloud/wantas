import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")
sys.path.append("/code")
import time
import os

from scrape_server import util
from scrape_server.store import AbsStore
from scrape_server import geo
from scrape_server.geo import StoreInfo
from scrape_server.database.db import JsonDbDriver


ROOT_URL = "https://www.mapion.co.jp"


def get_prefecture_urls() -> (list):
    """
    47都道府県のルートリンクのリストを返す。それぞれのページに市町村のリンクがある。
    """
    results = []
    for i in range(1, 48):
        # 1の位の場合初めに0を加える
        if len(str(i)) == 1:
            results.append(BASE_URL + "0" + str(i))
        else:
            results.append(BASE_URL + str(i))
    return results

def get_city_urls(prefecture_url) -> (list):
    """
    都道府県ページにある市町村事のリンクをリストで返す
    """
    results = []
    soup = get_soup(prefecture_url)
    city_tags = soup.findAll('li', attrs={"class", "list-3"})
    for tag in city_tags:
        city_url = tag.find('a', href=True)['href']
        results.append(ROOT_URL + city_url)
    return results

def get_store_urls(city_url) -> (list):
    """
    市町村ページにある店舗のリンクをリストで返す。
    """
    results = []
    soup = get_soup(city_url)
    store_tags = soup.findAll('table', attrs={"class", "list-table"})
    for tag in store_tags:
        for a_tag in tag.findAll('a', href=True):
            store_url = a_tag['href']
            results.append(ROOT_URL + store_url)
    return results


def get_store_info(store_url: str) -> (StoreInfo):
    """
    店舗のURLを受け取り、店名、住所をStoreクラスに格納し、Storeクラスを返す
    """
    """[summary]

    Returns:
        [type]: [description]
    """
    soup = get_soup(store_url)
    store_info_tag = soup.find('table', attrs={"class", "spot-table-basic tbl-basic"})
    td_tags = store_info_tag.findAll('td')
    store_name = td_tags[0].renderContents().decode('utf-8')
    address = td_tags[2].renderContents().decode('utf-8')
    return StoreInfo(store_name, address)

def register_database(json_path: str):
    """全国の店舗の情報をjsonに格納する
    呼び出し方
    BASE_URL = "https://www.mapion.co.jp/phonebook/M02005CM03/"
    get_soup = util.get_soup_wrapper(BASE_URL)
    register_database("famima_geo.json")

    progress_file_pathが常に進捗を管理するため、途中で止まっても、再度開始するだけで
    止まった場所からスタートする。

    Args:
        base_url (str): 全国コンビニサイトのurlを指定する
        json_path (str): 登録するjsonの名前
    """

    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), json_path)
    print(f"db_path: {db_path}")
    db = JsonDbDriver(db_path)
    progress_file_path = db_path + "_progress.json"
    print(f"progress_file: {progress_file_path}")
    if os.path.exists(progress_file_path):
        dic = util.read_json_file(progress_file_path)
        pre_s_idx = dic['pre']
        city_s_idx = dic['city']
        store_s_idx = dic['store']
    else:
        pre_s_idx = 0
        city_s_idx = 0
        store_s_idx = 0
    for i, pre in enumerate(get_prefecture_urls()[pre_s_idx:], start=pre_s_idx):
        for i2, city in enumerate(get_city_urls(pre)[city_s_idx:], start=city_s_idx):
            for i3, store in enumerate(get_store_urls(city)[store_s_idx:], start=store_s_idx):
                d = {"pre": i, "city": i2, "store": i3}
                util.write_json_file(progress_file_path, d)
                print(f"pre:   {pre},   i:  {i}")
                print(f"city:  {city},  i2: {i2}")
                print(f"store: {store}, i3: {i3}")
                store_info = get_store_info(store)
                db.put([store_info.__dict__])
                print(util.dict_to_json(store_info.__dict__))
            store_s_idx = 0
        city_s_idx = 0

if __name__ == '__main__':
    # command $ python3 get_store_geo.py familymart
    # util.solve_certificate_problem()
    config_dic = util.read_json_file("./config.json")
    store_name = sys.argv[1]
    if config_dic[store_name]:
        famima_dic = config_dic[store_name]
        BASE_URL = famima_dic['base_url']
        get_soup = util.get_soup_wrapper(BASE_URL)
        register_database(famima_dic['geo_file_name'])