import requests
from bs4 import BeautifulSoup
from typing import List
import time
import tqdm
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import util

def get_store_lat_lon(user_lat: float, user_lon: float) -> (float, float):
    # 近くのセブンを調べて店舗の位置を返す
    return 142.3, 23.3

def is_here(area: str, user_lat: float, user_lon: float) -> (bool):
    # area -> (例)全国、九州
    # 位置情報はareaの中に入っているか
    return True

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



