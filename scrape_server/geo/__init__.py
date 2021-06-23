import requests
from bs4 import BeautifulSoup
from typing import List
import time
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
from scrape_server import geo
from scrape_server.mylog import log
from scrape_server.database import db


class StoreInfo:
    """
    店名と住所、位置情報を格納するクラス
    """
    def __init__(self, name: str, address: str, lat=None, lon=None):
        self.name = name
        self.address = address
        log.debug(f"lat: {lat}")
        log.debug(f"lon: {lon}")
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


    
def get_most_near_store_info(user_lat: float, user_lon: float) -> (StoreInfo):
    """近くのセブンを調べて店舗の情報、位置を入れたStoreInfoクラスのインスタンスを返す。

    Args:
        user_lat (float, user_lon): ユーザーの位置情報

    Returns:
        StoreInfo: 位置情報などを入力されたStoreInfoクラスのインスタンスを返す
    """
    db2 = dataset.connect("sqlite:///" + os.path.join("database", "db.sqlite"))
    store_table = db2["store_info"]
    results = db.suited_store_table(store_table)

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
    match_ele = results[min_idx]
    log.debug(match_ele)
    return StoreInfo(match_ele['name'], match_ele['address'], match_ele['lat'], match_ele['lon'])

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

def absolutely_get_lat_lon(address: str) -> (float, float):
    """
    いろんな位置情報の取得方法を使用し、位置情報をとってくる。
    """
    log.debug("sleeping 10....")
    time.sleep(10)
    log.debug(f"find address: {address}.....")

    lat, lon = coordinate(address)
    if lat and lon:
        return lat, lon

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

def get_geo_soup(address: str, url: str):
    payload = {'q': address}
    html = requests.get(url, params=payload)
    return BeautifulSoup(html.content, "html.parser")

def coordinate(address: str):
    """
    addressに住所を指定すると緯度経度を返す。

    >>> coordinate('東京都文京区本郷7-3-1')
    ['35.712056', '139.762775']
    """
    url = 'http://www.geocoding.jp/api/'
    log.debug("invoked coordinate.")
    soup = get_geo_soup(address, url)
    if soup.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    lat_tg = soup.find('lat')
    lon_tg = soup.find('lon')

    if lat_tg == None or lon_tg == None:
        log.debug("failed")
        return 0.0, 0.0
    latitude = lat_tg.string
    longitude = lon_tg.string

    return [latitude, longitude]

def get_lat_lon(address: str) -> (float, float):
    log.debug("get_lat_lon")
    res = geocoder.osm(address, timeout=5.0)
    if res.latlng == None:
        log.debug("failed")
        return 0.0, 0.0
    lat, lon = res.latlng
    log.debug(f"lat: {lat}, lon: {lon}")
    return lat, lon

def get_lat_lon2(address: str) -> (float, float):
    log.debug("get_lat_lon2")
    log.debug("sleep 10....")
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
    log.debug("failed")
    return 0.0, 0.0

def get_lat_lon3(address: str) -> (float, float):
    log.debug("get_lat_lon3")
    locater = Nominatim(user_agent="test")
    location = locater.geocode(address)
    if location == None:
        log.debug("failed")
        return 0.0, 0.0
    log.debug(location)
    lat = location.latitude
    lon = location.longitude
    log.debug(f"lat: {lat}, lon: {lon}")
    return lat, lon

if __name__ == '__main__':
    pass
