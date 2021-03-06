import pytest
import sys
import requests
import time
import logging

from scrape_server import util
from scrape_server.store import familymart

BASE_URL = "https://www.family.co.jp"

def test_get_kind_of_products_listed_page():
    fam = familymart.FamilyMart()
    kind_of_products_listed_page = fam.get_kind_of_products_listed_page()
    assert BASE_URL in kind_of_products_listed_page

def test_get_kind_of_product_urls():
    fam = familymart.FamilyMart()
    get_soup = util.get_soup_wrapper(BASE_URL) # 必ず必要
    urls = fam.get_kind_of_product_urls(get_soup)
    assert 0 < len(urls)
    time.sleep(2)
    assert 200 == requests.get(urls[0]).status_code

def test_get_products_url_in_kind_of_product_url():
    fam = familymart.FamilyMart()
    get_soup = util.get_soup_wrapper(BASE_URL) # 必ず必要
    kind_of_urls = fam.get_kind_of_product_urls(get_soup)
    products_urls = fam.get_products_url_in_kind_of_product_url(kind_of_urls[7], get_soup)
    assert 0 < len(products_urls)
    time.sleep(2)
    assert 200 == requests.get(products_urls[7]).status_code

def test_is_available_kind_of_product_url():
    fam = familymart.FamilyMart()
    assert True == fam.is_available_kind_of_product_url("https://www.family.co.jp/goods/sidedishes.html")
    assert False == fam.is_available_kind_of_product_url("https://www.family.co.jp/goods/safety.html")

def test_Product_class():
    # スクレイピング結果は前回と異なる場合がある。
    fam = familymart.FamilyMart()
    get_soup = util.get_soup_wrapper(BASE_URL) # 必ず必要
    kind_of_urls = fam.get_kind_of_product_urls(get_soup)
    kind_of_product_url = "https://www.family.co.jp/goods/omusubi.html"
    products_urls = fam.get_products_url_in_kind_of_product_url(kind_of_product_url, get_soup)
    product = familymart.Product(products_urls[0])
    assert "product_name" in product.to_dict().keys()
    assert "product_url" in product.to_dict().keys()
    assert "product_price" in product.to_dict().keys()
    assert "product_region_list" in product.to_dict().keys()
    assert "product_img_url" in product.to_dict().keys()
    assert "store_table_name" in product.to_dict().keys()
    assert product.name != ""
    assert product.url != ""
    assert product.img_url != ""
    assert product.price != ""
    assert 0 < len(product.region_list)
    time.sleep(2)
    assert products_urls[0] == product.url
    assert 200 == requests.get(product.url).status_code
    time.sleep(2)
    assert 200 == requests.get(product.img_url).status_code