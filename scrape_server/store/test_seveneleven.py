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
    seven = seveneleven.SevenEleven()
    get_soup = util.get_soup_wrapper(BASE_URL)
    products_listed_page_urls = seven.get_products_listed_page_urls(get_soup)
    assert 0 < len(products_listed_page_urls)
    time.sleep(2)
    assert 200 == requests.get(products_listed_page_urls[0]).status_code

def test_get_products_soup_from_products_listed_page():
    seven = seveneleven.SevenEleven()
    get_soup = util.get_soup_wrapper(BASE_URL)
    url = "https://www.sej.co.jp/products/a/onigiri/"
    soup = get_soup(url)
    products_soup = seveneleven.get_products_soup_from_products_listed_page(soup)
    assert 18 == len(products_soup)

def test_Products_class():
    seven = seveneleven.SevenEleven()
    get_soup = util.get_soup_wrapper(BASE_URL)
    url = "https://www.sej.co.jp/products/a/onigiri/"
    soup = get_soup(url)
    products_soup = seveneleven.get_products_soup_from_products_listed_page(soup)
    products = seveneleven.Products(products_soup)
    assert 18 == len(products.contents)
    assert 18 == len(products.products_soup)
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
    assert "具たっぷり手巻　玉子かけ風ごはん" == product.name
    assert "https://www.sej.co.jp/products/a/item/045846" == product.url
    time.sleep(2)
    assert 200 == requests.get(product.url).status_code
    assert "120円（税込129.60円）" == product.price
    assert ['近畿'] == product.region_list
    assert "https://img.7api-01.dp1.sej.co.jp/item-image/045846/684810EEC1817DEF72475307B7281DF6.jpg" == product.img_url
    time.sleep(2)
    assert 200 == requests.get(product.img_url).status_code
    assert "store_seveneleven" == product.store_table_name