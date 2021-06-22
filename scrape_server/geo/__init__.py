import requests
from bs4 import BeautifulSoup
from typing import List
import time
import tqdm
import random
import datetime
import dataset
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")
import os
import geocoder
from geopy import geocoders
from geopy.geocoders import Nominatim

from scrape_server import util
from scrape_server.db_driver import DbDriver
from scrape_server import geo
from scrape_server.mylog import log
from scrape_server.database import database

class StoreInfo:
    """
    店名と住所、位置情報を格納するクラス
    """
    def __init__(self, name, address, lat=None, lon=None):
        self.name = name
        self.address = address
        print(f"lat: {lat}")
        print(f"lon: {lon}")
        if lat != None and lon != None:
            self.lat = float(lat)
            self.lon = float(lon)
        else:
            self.set_lat_lon()

    def set_lat_lon(self):
        try:
            self.lat, self.lon = geo.get_lat_lon2(self.address)
        except ValueError:
            self.lat, self.lon = 0,0


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

def suited_results(table: dataset.table.Table):
    """
    store_infoテーブル用。全てのレコードを取り出し、lat,lonをfloatにした要素を返す。
    """
    def suited(d: dict) -> (dict):
        new = {}
        for k, v in d.items():
            if k == "lat" or k == "lon":
                new[k] = float(v)
            else:
                new[k] = v
        return new

    results = [suited(d) for d in table.find()]
    return results


def get_most_near_store_info(user_lat: float, user_lon: float) -> (StoreInfo):
    """
    近くのセブンを調べて店舗の位置も含めた情報を返す
    """

    # get db 2
    db2 = dataset.connect("sqlite:///" + os.path.join("database", "db.sqlite"))
    store_table = db2["store_info"]
    results = suited_results(store_table)

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
    accord_ele = results[min_idx]
    print(util.dict_to_json(accord_ele))
    return StoreInfo(accord_ele['name'], accord_ele['address'], accord_ele['lat'], accord_ele['lon'])


def is_contains(area_list: str, store_info: StoreInfo) -> (bool):
    """
    店舗の場所はarea_listの中に入っているか
    area_list -> (例)全国、九州
    """
    log.debug("Invoked is_contains")
    log.debug(f"area_list: {area_list}")
    log.debug(f"store_info: {store_info}")
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
        if area in store_info.address:
            return True
        # areaが東北などの地域の場合
        for k, v in area_table.items():
            if area == k:
                for pre in v:
                    if pre in store_info.address:
                        return True
        if area == "全国":
            return True
    return False


URL = 'http://www.geocoding.jp/api/'
def absolutely_get_lat_lon(address) -> (float, float):
    print("sleeping 10....")
    print(datetime.datetime.now())
    time.sleep(10)
    print(f"find address: {address}.....")
    # lat, lon = coordinate(address)
    # if lat and lon:
        # return lat, lon

    lat, lon = get_lat_lon(address)
    if lat and lon:
        return lat, lon

    lat, lon = get_lat_lon2(address)
    if lat and lon:
        return lat, lon

    lat, lon = get_lat_lon3(address)
    if lat and lon:
        return lat, lon
    return 0.0, 0.0



def get_geo_soup(address, url):
    payload = {'q': address}
    html = requests.get(url, params=payload)
    return BeautifulSoup(html.content, "html.parser")


def coordinate(address):
    """
    addressに住所を指定すると緯度経度を返す。

    >>> coordinate('東京都文京区本郷7-3-1')
    ['35.712056', '139.762775']
    """
    print("*************************")
    print("coordinate")
    soup = get_geo_soup(address, URL)
    if soup.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    lat_tg = soup.find('lat')
    lon_tg = soup.find('lon')

    # while lat_tg == None or lon_tg == None:
    #     soup = get_geo_soup(address, URL)
    #     if soup.find('error'):
    #         raise ValueError(f"Invalid address submitted. {address}")
    #     lat_tg = soup.find('lat')
    #     lon_tg = soup.find('lon')
    #     print(f"address: {address}")
    #     print(f"lat_tg: {lat_tg}")
    #     print(f"lon_tg: {lon_tg}")
    #     time.sleep(10)
    if lat_tg == None or lon_tg == None:
        print("failed")
        return 0.0, 0.0
    latitude = lat_tg.string
    longitude = lon_tg.string

    return [latitude, longitude]

def get_lat_lon(address) -> (float, float):
    print("*************************")
    print("get_lat_lon")
    res = geocoder.osm(address, timeout=5.0)
    if res.latlng == None:
        print("failed")
        return 0.0, 0.0
    lat, lon = res.latlng
    print("lat: {lat}, lon: {lon}")
    return lat, lon


def get_lat_lon2(address) -> (float, float):
    print("*****************************")
    print("get_lat_lon2")
    print("sleep 10 ...")
    time.sleep(10)
    url = 'http://www.geocoding.jp/'
    soup = get_geo_soup(address, url)
    tags = soup.findAll('span', attrs={"class", "nowrap"})
    for t in tags:
        if "緯度" in str(t) or "経度" in str(t):
            b_tag = t.findAll('b')
            lat = b_tag[0].next_element
            lon = b_tag[1].next_element
            return lat, lon
    print("failed")
    return 0.0, 0.0

def get_lat_lon3(address) -> (float, float):
    print("*****************************")
    print("get_lat_lon3")
    locater = Nominatim(user_agent="test")
    # geolocator = geocoders.GoogleV3()
    location = locater.geocode(address)
    if location == None:
        print("failed")
        return 0.0, 0.0
    print(location)
    lat = location.latitude
    lon = location.longitude
    print(f"lat: {lat}, lon: {lon}")
    return lat, lon

if __name__ == '__main__':
    address = "福島県河沼郡湯川村浜崎水上１４１３−２"
    lat, lon = absolutely_get_lat_lon(address)
    print("-------- result ---------")
    print(f"lat: {lat}, lon: {lon}")
