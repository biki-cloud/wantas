import pytest
import sys
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")
import requests
import time
import logging
from bs4 import BeautifulSoup
import bs4

from scrape_server import util
from scrape_server.store import seveneleven

BASE_URL = "https://www.sej.co.jp"

@pytest.mark.large
def test_get_products_listed_page_urls():
    # 時間がかかりすぎる
    assert True
    # seven = seveneleven.SevenEleven()
    # get_soup = util.get_soup_wrapper(BASE_URL)
    # products_listed_page_urls = seven.get_products_listed_page_urls(get_soup)
    # assert 0 < len(products_listed_page_urls)
    # time.sleep(2)
    # assert 200 == requests.get(products_listed_page_urls[0]).status_code

def test_get_products_soup_from_products_listed_page():
    seven = seveneleven.SevenEleven()
    get_soup = util.get_soup_wrapper(BASE_URL)
    url = "https://www.sej.co.jp/products/a/onigiri/"
    soup = get_soup(url)
    products_soup = seveneleven.get_products_soup_from_products_listed_page(soup)
    assert 0 < len(products_soup)

def test_Products_class():
    seven = seveneleven.SevenEleven()
    get_soup = util.get_soup_wrapper(BASE_URL)
    url = "https://www.sej.co.jp/products/a/onigiri/"
    soup = get_soup(url)
    products_soup = seveneleven.get_products_soup_from_products_listed_page(soup)
    products = seveneleven.Products(products_soup)
    assert 0 < len(products.contents)
    assert 0 < len(products.products_soup)
    assert type(products.products_soup[0]) is bs4.element.Tag
    assert type(products.get_contents()[0]) is seveneleven.Product

def test_Product_class():
    seven = seveneleven.SevenEleven()
    get_soup = util.get_soup_wrapper(BASE_URL)
    url = "https://www.sej.co.jp/products/a/onigiri/"
    soup = get_soup(url)
    products_soup = seveneleven.get_products_soup_from_products_listed_page(soup)
    products = seveneleven.Products(products_soup)
    product = products.get_contents()[0]
    assert product.name != ""
    assert product.url != ""
    time.sleep(2)
    assert 200 == requests.get(product.url).status_code
    assert product.price != ""
    assert 0 < len(product.region_list)
    assert product.img_url != ""
    time.sleep(2)
    assert 200 == requests.get(product.img_url).status_code
    assert "store_seveneleven" == product.store_table_name