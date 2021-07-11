import requests
from bs4 import BeautifulSoup
from typing import List
import time
import random
import datetime
import dataset
import sys
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")
import os

from scrape_server import util
from scrape_server import geo
from scrape_server.mylog import log
from scrape_server.database import db


class StoreInfo:
    """
    店名と住所、位置情報を格納するクラス
    """
    def __init__(self, name: str, address: str, lat=None, lon=None):
        self.store_name = name
        self.store_address = address
        log.debug(f"lat: {lat}")
        log.debug(f"lon: {lon}")
        if lat != None and lon != None:
            self.store_lat = float(lat)
            self.store_lon = float(lon)
        else:
            self.set_lat_lon()

    def set_lat_lon(self):
        try:
            self.store_lat, self.store_lon = geo.get_lat_lon2(self.store_address)
        except ValueError:
            self.store_lat, self.store_lon = 0,0


def is_lat(lat) -> (bool):
    return lat > -45 and lat < 45

def is_lon(lon) -> (bool):
    return lon > -180 and lon < 180


def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> (float):
    """2つの位置情報(lat,lon)をもらい、その距離を返す。

    Args:
        lat1 (float): lat 1
        lat2 (float): lat 2
        lon1 (float): lon 1
        lon2 (float): lon 2

    Raises:
        ValueError: 引数のどれかが適切な値でない場合、エラーを起こす

    Returns:
        float: lat同士の距離とlon同士の距離を足したもの
    """
    if is_lat(lat1) and is_lat(lat2) and is_lon(lon1) and is_lon(lon2):
        lat_dis = lat1 - lat2
        if lat_dis < 0:
            lat_dis = -lat_dis

        lon_dis = lon1 - lon2
        if lon_dis < 0:
            lon_dis = -lon_dis

        return lat_dis + lon_dis
    else:
        raise ValueError(f"invalid value lat or lon. lat1: {lat1}, lon1: {lon1}, lat2: {lat2}, lon2: {lon2}")


def get_most_near_store_info(user_lat: float, user_lon: float, store_table_name: str) -> (StoreInfo):
    """近くのセブンを調べて店舗の情報、位置を入れたStoreInfoクラスのインスタンスを返す。

    Args:
        user_lat (float, user_lon): ユーザーの位置情報
        store_type: 店のタイプ, familymart, sevenelevenのみ今は。

    Returns:
        StoreInfo: 位置情報などを入力されたStoreInfoクラスのインスタンスを返す
    """
    db2 = dataset.connect(f"sqlite:///{os.path.abspath(os.path.dirname(__file__))}/../database/db.sqlite")

    store_table = db2[store_table_name]
    results = db.suited_store_table(store_table)

    distances = []
    for store in results:
        dic = {}
        store_lat = float(store['store_lat'])
        store_lon = float(store['store_lon'])
        dic['store_lat'] = store_lat
        dic['store_lon'] = store_lon
        dic['distance'] = get_distance(user_lat, user_lon, store_lat, store_lon)
        distances.append(dic)

    # ユーザーと距離が最短の店舗を探す
    min_dis = 100.0 # 初期値
    min_idx = 0 # 初期値
    for idx, dis_dict in enumerate(distances):
        if dis_dict['distance'] < min_dis:
            min_dis = dis_dict['distance']
            min_idx = idx
    match_ele = results[min_idx]
    return StoreInfo(match_ele['store_name'], match_ele['store_address'], match_ele['store_lat'], match_ele['store_lon'])

def is_contains(product_store_dic: dict) -> (bool):
    """
    店舗の場所はarea_listの中に入っているか
    area_list -> (例)[全国、九州]
    """
    log.debug("Invoked is_contains")
    log.debug(f"area_list: {product_store_dic['product_region_list']}")
    area_table = {
        "北海道": ["北海道"],
        "東北": ["青森", "岩手", "宮城", "秋田", "山形", "福島"],
        "関東": ["埼玉", "千葉", "東京", "神奈川", "茨城", "栃木", "群馬", "山梨", "長野"],
        "南関東": ["埼玉", "千葉", "東京", "神奈川"],
        "北関東": ["茨城", "栃木", "群馬", "山梨", "長野"],
        "甲信": ["茨城", "栃木", "群馬", "山梨", "長野"],
        "北陸": ["新潟", "富山", "石川", "福井"],
        "東海": ["岐阜", "静岡", "愛知", "三重"],
        "近畿": ["滋賀", "京都", "大阪", "兵庫", "奈良", "和歌山"],
        "中国": ["鳥取", "島根", "岡山", "広島", "山口"],
        "四国": ["徳島", "香川", "愛媛", "高知"],
        "中四国": ["鳥取", "島根", "岡山", "広島", "山口", "徳島", "香川", "愛媛", "高知"],
        "九州": ["福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄"],
        "北九州": ["福岡", "佐賀", "長崎", "熊本", "大分"],
        "南九州": ["宮崎", "鹿児島"],
        "首都圏": ["埼玉", "千葉", "神奈川", "東京"]
    }
    # 店の住所
    store_address = product_store_dic['store_address']
    # ['中国', '熊本', '鹿児島']みたいな販売されているエリア
    product_region_list = product_store_dic['product_region_list']
    log.debug(f"store_address: {store_address}")
    log.debug(f"product_region_list: {product_region_list}")

    for area in product_region_list:
        # TODO: areaの一文字目に!が入っていたらその地域意外となる。
        # 販売地域リストの一つが県名で店の住所文字列の中に入っていればそこでは販売されている
        if area[0] == "!":
            if area[1:] not in store_address:
                return True
            else:
                return False
        elif area in store_address:
            return True
        # areaが中国などの地域の場合
        for k, v in area_table.items():
            if area == k:
                for pre in v:
                    # 中国だと"鳥取", "島根", "岡山", "広島", "山口"のどれかが店の住所文字列に入っていればそこでは販売されている
                    if pre in store_address:
                        return True
        if area == "全国":
            return True
    return False

def get_geo_soup(address: str, url: str):
    time.sleep(1)
    payload = {'q': address}
    html = requests.get(url, params=payload)
    return BeautifulSoup(html.content, "html.parser")

def get_lat_lon2(address: str) -> (float, float):
    log.debug("get_lat_lon2")
    url = 'http://www.geocoding.jp/'
    while True:
        soup = get_geo_soup(address, url)
        if "該当する住所が見つかりませんでした。" in str(soup):
            return 0.0, 0.0
        tags = soup.findAll('span', attrs={"class", "nowrap"})
        for t in tags:
            if "緯度" in str(t) or "経度" in str(t):
                b_tag = t.findAll('b')
                lat = b_tag[0].next_element
                lon = b_tag[1].next_element
                return float(lat), float(lon)
        print(f"it seems too many request.{time.asctime()} sleep 2")
        time.sleep(2)
    log.debug("failed")

if __name__ == '__main__':
    pass
