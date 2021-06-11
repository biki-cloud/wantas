import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")
import time
import os

from scrape_server import util
from scrape_server import geo
from scrape_server.db_driver import DbDriver


ROOT_URL = "https://www.mapion.co.jp"
BASE_URL = "https://www.mapion.co.jp/phonebook/M02005CM01/"

def get_prefecture_urls() -> (list):
    """
    47都道府県のルートリンクのリストを返す。それぞれのページに市町村のリンクがある。
    """
    results = []
    for i in range(8, 48):
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
    soup = util.get_soup(prefecture_url)
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
    soup = util.get_soup(city_url)
    store_tags = soup.findAll('table', attrs={"class", "list-table"})
    for tag in store_tags:
        for a_tag in tag.findAll('a', href=True):
            store_url = a_tag['href']
            results.append(ROOT_URL + store_url)
    return results


class Store:
    """
    店名と住所、位置情報を格納するクラス
    """
    def __init__(self, store_name, address):
        self.store_name = store_name
        self.address = address
        self.set_lat_lon()

    def set_lat_lon(self):
        try:
            self.lat, self.lon = geo.coordinate(self.address)
        except ValueError:
            self.lat, self.lon = 0,0


def get_store_info(store_url) -> (Store):
    """
    店舗のURLを受け取り、店名、住所をStoreクラスに格納し、Storeクラスを返す
    """
    soup = util.get_soup(store_url)
    store_info_tag = soup.find('table', attrs={"class", "spot-table-basic tbl-basic"})
    td_tags = store_info_tag.findAll('td')
    store_name = td_tags[0].renderContents().decode('utf-8')
    address = td_tags[2].renderContents().decode('utf-8')
    return Store(store_name, address)

def register_database(interval=1):
    """
    全国の店舗の情報をgeo_database.jsonに格納していく
    """
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geo_database.json")
    db = DbDriver(db_path)
    stores: List[Store] = []
    for pre in get_prefecture_urls():
        for city in get_city_urls(pre):
            for store in get_store_urls(city):
                store_info = get_store_info(store)
                db.put([store_info.__dict__])
                print(util.dict_to_json(store_info.__dict__))
                stores.append(store_info)
                time.sleep(interval)

def main():
    register_database()


if __name__ == '__main__':
    main()