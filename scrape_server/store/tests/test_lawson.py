from bs4 import BeautifulSoup
import sys
import requests
import time

from scrape_server.store import lawson


BASE_URL = "https://www.lawson.co.jp"


def test_Product_class():
    b = BeautifulSoup("""<li>
                    <p class="img"><a href="/recommend/original/detail/1430800_1996.html"><img alt="おにからセット(シーチキンマヨネーズ・日高昆布)" height="169" src="/recommend/original/detail/img/l650329.jpg" width="220"/></a></p>
                    <p class="ttl">おにからセット(シーチキンマヨネーズ・日高昆布)</p>
                    <p>452kcal</p>
                    <p class="price"><span>298円</span><span>(税込)</span></p>
                    <p class="smalltxt" style="padding-top:5px;">※近畿・中四国地域のローソンではお取り扱いしておりません。</p>
                    </li>""", features="html.parser")
    product = lawson.Product(b)
    assert '298円(税込)' == product.price
    assert "おにからセット(シーチキンマヨネーズ・日高昆布)" == product.name
    assert BASE_URL + "/recommend/original/detail/1430800_1996.html" == product.url
    time.sleep(2)
    assert 200 == requests.get(product.url).status_code
    assert BASE_URL + "/recommend/original/detail/img/l650329.jpg" == product.img_url
    time.sleep(2)
    assert 200 == requests.get(product.img_url).status_code
    assert ["!近畿", "!中四国"] == product.region_list
    assert "store_lawson" == product.store_table_name

def test_get_all_type_of_product_urls():
    lawson_obj = lawson.Lawson()
    urls = lawson_obj.get_all_type_of_product_urls()
    assert 0 < len(urls)
    time.sleep(2)
    assert 200 == requests.get(urls[0]).status_code

def test_get_product_infos_from_type_of_product_url():
    lawson_obj = lawson.Lawson()
    all_type_of_product_urls = lawson_obj.get_all_type_of_product_urls()
    product_infos = lawson_obj.get_product_infos_from_type_of_product_url(all_type_of_product_urls[0])
    assert 20 < len(product_infos)


