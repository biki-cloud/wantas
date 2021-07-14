import sys
import time
from typing import List
import bs4
from collections.abc import Callable
from bs4 import BeautifulSoup
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")

from scrape_server import util
from scrape_server.store import AbsStore

BASE_URL = "https://www.sej.co.jp"
get_soup = util.get_soup_wrapper(BASE_URL) #必ず必要

class Product:
    """
    商品情報のbs4.element.Tagを受け取り、名前、値段、urlなどを格納するクラス
    """

    def __init__(self, item: bs4.element.Tag):
        self.item = item
        self.name = self.get_name()
        self.url = self.get_url()
        self.price = self.get_price()
        self.region_list = self.get_region()
        self.img_url = self.get_img_url()
        self.store_table_name = "store_seveneleven"

    def __repr__(self):
        return str(self.item)

    def __str__(self):
        return str(self.item)

    def get_tag(self):
        return self.item

    def to_dict(self) -> (dict):
        """Productインスタンスがもつプロパティをdictにして返す。

        Returns:
            dict: {
                "name": "商品の名前",
                "url": "商品ページのurl",
                "price": "商品の値段",
                "region_list": "売られている地域のリスト",
                "img_url": "画像のaddress"
            }
        """
        return {
            "product_name": self.name,
            "product_url": self.url,
            "product_price": self.price,
            "product_region_list": self.region_list,
            "product_img_url": self.img_url,
            "store_table_name": self.store_table_name
        }

    def get_name(self) -> (str):
        title_tag = self.item.find('div', attrs={"class", "item_ttl"})
        return title_tag.string

    def get_url(self) -> (str):
        title_tag = self.item.find('div', attrs={"class", "item_ttl"})
        url = title_tag.find('a', href=True)['href']
        seven = SevenEleven()
        url = util.url_join(seven.base_url, url)
        return url

    def get_price(self) -> (str):
        price_tag = self.item.find('div', attrs={"class", "item_price"})
        return price_tag.string

    def get_region(self) -> (list):
        region_tag = self.item.find('div', attrs={"class", "item_region"})
        p_tag = region_tag.find('p')
        region_str = p_tag.getText()
        deleted_str = region_str.replace("販売地域：", "")
        return deleted_str.split("、")

    def get_img_url(self) -> (str):
        img_tag = self.item.find('img')
        img_url = img_tag['data-original']
        return img_url

    def display_properties(self):
        for k, v in self.to_dict.items():
            print(f"{k}: {v}")


class Products:
    """
    Productクラスをリストで保持するクラス
    """

    def __init__(self, products_soup: bs4.element.ResultSet):
        self.products_soup: List[bs4.element.Tag] = [i for i in products_soup]
        self.contents = [Product(item_tag) for item_tag in self.products_soup]

    def get_contents(self) -> (List[Product]):
        return self.contents


class ProductKinds:
    """
    セブンイレブンの全ての商品の種類をプロパティとして保持するクラス
    """

    def __init__(self):
        self.thisweek = "thisweek"
        self.nextweek = "nextweek"
        self.onigiri = "onigiri"
        self.sushi = "sushi"
        self.bento = "bento"
        self.sandwich = "sandwich"
        self.bread = "bread"
        self.donut = "donut"
        self.men = "men"
        self.pasta = "pasta"
        self.gratin = "gratin"
        self.dailydish = "dailydish"
        self.salad = "salad"
        self.sweets = "sweets"
        self.ice_cream = "ice_cream"
        self.hotsnack = "hotsnack"
        self.oden = "oden"
        self.chukaman = "chukaman"
        self.sevencafe = "sevencafe"
        self.seven_premium = "7premium"
        self.hotsnack = "hotsnack"


class Area:
    """
    セブンイレブンの全ての地域のプロパティを保持するクラス
    """

    def __init__(self):
        self.okinawa = "okinawa"
        self.kyushu = "kyushu"
        self.shikoku = "shikoku"
        self.chugoku = "chugoku"
        self.kinki = "kinki"
        self.hokuriku = "hokuriku"
        self.koshinetsu = "koshinetsu"
        self.kanto = "kanto"
        self.tohoku = "tohoku"
        self.hokkaido = "hokkaido"


def get_products_soup_from_products_listed_page(soup) -> (bs4):
    """商品がリストで掲載されているページの中から商品情報のsoupを全て取得し、bs4インスタンスで返す.
    example url: https://www.sej.co.jp/products/a/onigiri/

    Args:
        soup (BeautifulSoup): 商品がリストで掲載されているページ全体のBeautifulSoupインスタンス

    Returns:
        BeautifulSoup: 商品がリストで掲載されているページの中から商品情報のsoupを全て取得し、bs4インスタンスで返す
    """
    return soup.findAll("div", {"class": "list_inner"})


class SevenEleven(AbsStore):
    """
    セブンイレブンのサイトをスクレイピングするクラス。Storeクラスを継承していて、get_all_productを実装しなければならない。
    """

    def __init__(self):
        self.base_url = "https://www.sej.co.jp"
        self.products = "products"
        self.a = "a"
        self.area = "area"
        self.product_kind = ProductKinds()
        self.areas = Area()

    def get_product_url(self, product_name: str):
        res = self.product_kind.__dict__.get(product_name)
        if res:
            return util.url_join(self.base_url, self.products, self.a, res)
        return ""

    def get_recursive_links(self, link: str, all_links: list, get_soup: Callable[[str], BeautifulSoup]) -> (None):
        """商品リストが掲載されているページにはラインナップボタンや、1,2,3..のようなボタンがある。
        その中を探索していき商品がリストで掲載されているページurlを取得していく。

        Args:
            link (str): 適当なurl
            all_links (list): 探索しながら取得したurlを追加していくリスト
        """
        if link not in all_links:
            all_links.append(link)

            line_up_links = self.get_line_up_links(link, get_soup)
            for l in line_up_links:
                self.get_recursive_links(l, all_links, get_soup)

            pager_links = self.get_pager_links(link)
            for l in pager_links:
                self.get_recursive_links(l, all_links, get_soup)
        return

    def get_products_listed_page_urls(self, get_soup: Callable[[str], BeautifulSoup]) -> (list):
        """セブンイレブンの商品がリストで掲載されているのページurl全てをリストにして返す。
        page example: https://www.sej.co.jp/products/a/onigiri/

        Returns:
            list: urlのリストを返す。
        """
        results = []
        all_product_kind = self.product_kind.__dict__.keys()
        for product in all_product_kind:
            product_url = self.get_product_url(product)
            self.get_recursive_links(product_url, results, get_soup)
        return results

    def get_line_up_links(self, url: str, get_soup: Callable[[str], BeautifulSoup]) -> (list):
        """urlページの中に"ラインナップを見る"ボタンが複数あるだけそのボタンのリンク先urlのリストを返す。

        Args:
            url (str): 適当なセブンイレブンのページurl

        Returns:
            list: ラインナップのurl先のリストを返す
        """
        result_links = []
        soup = get_soup(url)
        line_up_elements = soup.find_all(class_="list_btn brn pbNested pbNestedWrapper")
        for ele in line_up_elements:
            url = util.url_join(self.base_url, ele.find('a', href=True)['href'])
            result_links.append(url)
        return result_links

    def get_pager_links(self, url: str) -> (list):
        """urlページの中に1,2,3,4のようなページに収まりきれずに複数ページになっているもののリンクを全て取得し、リストで返す。

        Args:
            url (str): 適当なセブンイレブンのページ

        Returns:
            list: 複数ページになっているリンクurlのリストを返す。
        """
        result_links = []
        soup = get_soup(url)
        pager_elements = soup.find_all(class_="pager_num")
        for ele in pager_elements:
            if ele not in result_links:
                a_tag = ele.find("a")
                if a_tag:
                    url = util.url_join(self.base_url, a_tag.get('href'))
                    result_links.append(url)
        return result_links

    def get_all_product(self) -> (list):
        """全商品をスクレイピングし、dictにしそれをリストにして返す。
        店舗ごとにクラスを作成する場合にこのメソッドを実装しなければならない

        Returns:
            list: 下のようなdictのリストを返す。
            example: {
                name: 商品の名前,
                url: 商品ページのurl,
                price: 商品の価格,
                region_list: 販売地域のリスト,
                img_url: 商品画像のurl
            }
        """
        get_soup = util.get_soup_wrapper(BASE_URL) #必ず必要
        results = []
        products_listed_page_urls = self.get_products_listed_page_urls(get_soup)
        for products_listed_url in products_listed_page_urls:
            soup = get_soup(products_listed_url)
            products_soup = get_products_soup_from_products_listed_page(soup)
            products = Products(products_soup)
            for product in products.get_contents():
                dic = product.to_dict()
                print(util.dict_to_json(dic))
                # prevent to insert same product.
                if dic['product_name'] not in [i['product_name'] for i in results]:
                    results.append(dic)
        return results


if __name__ == '__main__':
    # util.solve_certificate_problem()
    seven = SevenEleven()
    results = seven.get_all_product()
    util.write_json_file("./product_seveneleven.json", results)

