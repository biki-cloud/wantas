import sys
import pytest
from bs4 import BeautifulSoup
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")

from scrape_server import geo
from scrape_server import store

@pytest.mark.parametrize(
    "dic, r", [
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["埼玉", "熊本", "静岡"]
        }, True),
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["関東", "熊本", "静岡"]
        }, True),
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["!熊本"]
        }, True),
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["!熊本", "!埼玉"]
        }, False),
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["!埼玉"]
        }, False),
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["!埼玉", "関東"]
        }, False),
        ({
            "store_address": "神奈川県ふじみ野市",
            "product_region_list": ["!埼玉", "関東"]
        }, True),
        ({
            "store_address": "滋賀県ふじみ野市",
            "product_region_list": ['!近畿', '!中四国']
        }, False)
    ]
)
def test_is_contains(dic, r):
    assert r == geo.is_contains(dic)


@pytest.mark.parametrize(
    "lat, r", [
        (35.43434, True),
        (73.43425, False),
        (-23.4343, True),
        (-74.4343, False)
    ]
)
def test_is_lat(lat, r):
    assert r == geo.is_lat(lat)


@pytest.mark.parametrize(
    "lon, r", [
        (140.43434, True),
        (-130.43425, True),
        (-23.4343, True),
        (190.43242, False)
    ]
)
def test_is_lon(lon, r):
    assert r == geo.is_lon(lon)


@pytest.mark.parametrize(
    "lat1, lon1, lat2, lon2, r", [
        (35.4343, 140.3232, 35.43243, 134.423434, 5.901636000000032),
        (32.2948, 144.42892, 39.3883, 138.423434, 13.098986000000018)
    ]
)
def test_get_distance(lat1, lon1, lat2, lon2, r):
    assert r == geo.get_distance(lat1, lon1, lat2, lon2)


@pytest.mark.parametrize(
    "user_lat, user_lon, store_table_name, r", [
        (35.43343434, 140.43434, "store_familymart", geo.StoreInfo("ファミリーマート長生一松海岸店", "千葉県長生郡長生村驚５７７", 35.414682, 140.389927)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
        (38.4343, 144.333, "store_seveneleven", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279)),
    ]
)
def test_get_most_near_store_info(user_lat, user_lon, store_table_name, r):
    assert r.store_address == geo.get_most_near_store_info(user_lat, user_lon, store_table_name).store_address
    # assert r.store_name == geo.get_most_near_store_info(user_lat, user_lon, store_table_name).store_name
    # assert r.store_lat == geo.get_most_near_store_info(user_lat, user_lon, store_table_name).store_lat
    # assert r.store_lon == geo.get_most_near_store_info(user_lat, user_lon, store_table_name).store_lon


@pytest.mark.parametrize(
    "address, r", [
        ("千葉県長生郡長生村驚５７７", ("35.414682", "140.389927")),
        ("宮城県牡鹿郡女川町大道１−２", ("38.439817", "141.440279"))
    ]
)
def test_get_lat_lon2(address, r):
    assert r == geo.get_lat_lon2(address)


@pytest.mark.parametrize(
    "address, url, r", [
        ("千葉県長生郡長生村驚５７７", 'http://www.geocoding.jp/', BeautifulSoup)
    ]
)
def test_get_geo_soup(address, url, r):
    assert type(geo.get_geo_soup(address, url)) == r


@pytest.mark.parametrize(
    "name, address, r", [
    ("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", geo.StoreInfo("セブンイレブン女川バイパス店", "宮城県牡鹿郡女川町大道１−２", 38.439817, 141.440279))
    ]
)
def test_StoreInfo_class(name, address, r):
    store_info = geo.StoreInfo(name, address)
    assert r.store_name == store_info.store_name
    assert r.store_address == store_info.store_address
    assert r.store_lat == store_info.store_lat
    assert r.store_lon == store_info.store_lon