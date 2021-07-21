import pytest
import sys
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")
sys.path.append("/home/hibiki/wantas/scrape_server")
import os
import requests
import time

from scrape_server import geo
from scrape_server.geo import get_store_geo
from scrape_server import util

ROOT_URL = "https://www.mapion.co.jp"

def test_config_json_is_available():
    config_json_path = f"{os.path.abspath(os.path.dirname(__file__))}/config.json"
    # config_json_path = "./config.json"
    assert os.path.exists(config_json_path)
    dict_content = util.read_json_file(config_json_path)
    assert type(dict_content) is dict
    for k, v in dict_content.items():
        assert "familymart" == k or "seveneleven" == k or "lawson" == k
        assert "base_url" in v
        assert "geo_file_name" in v


@pytest.mark.parametrize(
    "base_url, r", [
        ("https://www.mapion.co.jp/phonebook/M02005CM01/", 47),
        ("https://www.mapion.co.jp/phonebook/M02005CM02/", 47),
        ("https://www.mapion.co.jp/phonebook/M02005CM03/", 47),
        ("https://www.mapion.co.jp/phonebook/M02005CM04/", 47)
    ]
)
def test_get_prefecture_urls(base_url, r):
    assert r == len(get_store_geo.get_prefecture_urls(base_url))
    time.sleep(2)
    assert 503 == requests.get(base_url).status_code


def test_get_city_urls():
    base_url = "https://www.mapion.co.jp/phonebook/M02005CM01/"
    get_soup = util.get_soup_wrapper(base_url)
    pre_url = get_store_geo.get_prefecture_urls(base_url)[0]
    city_urls = get_store_geo.get_city_urls(pre_url, get_soup)
    for url in city_urls:
        assert base_url in url
    time.sleep(2)
    res = requests.get(city_urls[0])
    assert 503 == res.status_code

def test_get_store_urls():
    base_url = "https://www.mapion.co.jp/phonebook/M02005CM01/"
    get_soup = util.get_soup_wrapper(base_url)
    pre_url = get_store_geo.get_prefecture_urls(base_url)[0]
    city_urls = get_store_geo.get_city_urls(pre_url, get_soup)[0]
    store_urls = get_store_geo.get_store_urls(city_urls, get_soup)
    time.sleep(2)
    res = requests.get(store_urls[0])
    assert 503 == res.status_code


@pytest.mark.parametrize(
    "base_url, r", [
        ("https://www.mapion.co.jp/phonebook/M02005CM01/", geo.StoreInfo("セブンイレブン愛別町店", '北海道上川郡愛別町本町１４０', 43.908554, 142.573098)),
        ("https://www.mapion.co.jp/phonebook/M02005CM02/", geo.StoreInfo("ローソン赤平幌岡店", '北海道赤平市幌岡町５４', 43.579571, 142.037059)),
    ]
)
def test_get_store_info(base_url, r):
    get_soup = util.get_soup_wrapper(base_url)
    pre_url = get_store_geo.get_prefecture_urls(base_url)[0]
    city_urls = get_store_geo.get_city_urls(pre_url, get_soup)[0]
    store_urls = get_store_geo.get_store_urls(city_urls, get_soup)
    store_url = store_urls[0]
    assert r.store_address == get_store_geo.get_store_info(store_url, get_soup).store_address
    assert r.store_name == get_store_geo.get_store_info(store_url, get_soup).store_name
    assert r.store_lat == get_store_geo.get_store_info(store_url, get_soup).store_lat
    assert r.store_lon == get_store_geo.get_store_info(store_url, get_soup).store_lon