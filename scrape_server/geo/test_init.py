import sys
import pytest
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")

from scrape_server import geo

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
            "product_region_list": ["!埼玉"]
        }, False),
        ({
            "store_address": "埼玉県ふじみ野市",
            "product_region_list": ["!埼玉", "関東"]
        }, False),
        ({
            "store_address": "神奈川県ふじみ野市",
            "product_region_list": ["!埼玉", "関東"]
        }, True)
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
        (35.43343434, 140.43434, "familymart", "埼玉県ふじみ野市")
    ]
)
def test_get_most_near_store_info(user_lat, user_lon, store_table_name, r):
    assert r == geo.get_most_near_store_info(user_lat, user_lon, store_table_name)