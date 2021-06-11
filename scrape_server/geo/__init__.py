import requests
from bs4 import BeautifulSoup
from typing import List
import time
import tqdm
import random
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")
import os

from scrape_server import util
from scrape_server.db_driver import DbDriver


def is_lat(lat) -> (bool):
    return lat > -45 and lat < 45

def is_lon(lon) -> (bool):
    return lon > -180 and lon < 180

def get_distance(lat1, lon1, lat2, lon2) -> (float):
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

def get_shortest_store_info(user_lat: float, user_lon: float) -> (dict):
    """
    近くのセブンを調べて店舗の位置も含めた情報を返す
    """
    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geo_database.json")
    db_driver = DbDriver(database_path)
    results = db_driver.get_all()
    distances = []
    for store in results:
        dic = {}
        store_lat = float(store['lat'])
        store_lon = float(store['lon'])
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
    return results[min_idx]


def is_contains(area_list: str, store_info: dict) -> (bool):
    """
    店舗の場所はarea_listの中に入っているか
    area_list -> (例)全国、九州
    """
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
        "九州": ["福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄"],
        "首都圏": ["埼玉", "千葉", "神奈川", "東京"]
    }

    for area in area_list:
        # areaが県の場合
        if area in store_info['address']:
            return True
        # areaが東北などの地域の場合
        for k, v in area_table.items():
            if area == k:
                for pre in v:
                    if pre in store_info['address']:
                        return True
        if area == "全国":
            return True
    return False


URL = 'http://www.geocoding.jp/api/'

def coordinate(address):
    """
    addressに住所を指定すると緯度経度を返す。

    >>> coordinate('東京都文京区本郷7-3-1')
    ['35.712056', '139.762775']
    """
    payload = {'q': address}
    html = requests.get(URL, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    latitude = soup.find('lat').string
    longitude = soup.find('lng').string
    return [latitude, longitude]


def coordinates(addresses, interval=10, progress=True):
    """
    addressesに住所リストを指定すると、緯度経度リストを返す。

    >>> coordinates(['東京都文京区本郷7-3-1', '東京都文京区湯島３丁目３０−１'], progress=False)
    [['35.712056', '139.762775'], ['35.707771', '139.768205']]
    """
    coordinates = []
    for address in progress and tqdm(addresses) or addresses:
        coordinates.append(coordinate(address))
        time.sleep(interval)
    return coordinates

if __name__ == '__main__':
    print(get_shortest_store_info(43.23422, 144.332342))

