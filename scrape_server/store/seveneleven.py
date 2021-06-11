import time
from typing import List
import bs4
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import util
from scrape_server import geo
from scrape_server import db_driver as db
from scrape_server.store import Store


class Items:
    """
    Itemクラスをリストで保持するクラス
    """
    def __init__(self, items_div: bs4.element.ResultSet):
        self.items_div: List[bs4.element.Tag] = [i for i in items_div]
        self.items = [Item(item_tag) for item_tag in self.items_div]


class Item:
    """
    商品情報のbs4.element.Tagを受け取り、名前、値段、urlなどを格納するクラス
    """
    def __init__(self, item: bs4.element.Tag):
        self.item = item
        self.title = self.get_title()
        self.url = self.get_url()
        self.price = self.get_price()
        self.region_list = self.get_region()

    def __repr__(self):
        return str(self.item)

    def __str__(self):
        return str(self.item)

    def get_tag(self):
        return self.item

    def to_dict(self) -> (dict):
        return {
            "name": self.title,
            "url": self.url,
            "price": self.price,
            "region_list": self.region_list
        }

    def get_title(self) -> (str):
        title_tag = self.item.find('div', attrs={"class", "item_ttl"})
        return title_tag.string

    def get_url(self) -> (str):
        title_tag = self.item.find('div', attrs={"class", "item_ttl"})
        url = title_tag.find('a', href=True)['href']
        seven = SevenEleven()
        url = util.join_slash(seven.base_url, url)
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

    def display_properties(self):
        for k, v in self.to_dict.items():
            print(f"{k}: {v}")


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


class SevenEleven(Store):
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

    @classmethod
    def get_items_tag_from_page(cls, soup) -> (bs4.element.ResultSet):
        return soup.findAll("div", {"class": "list_inner"})

    def get_area_url(self, area_name):
        res = self.areas.__dict__.get(area_name)
        if res:
            return util.join_slash(self.base_url, self.products, self.a, self.product_kind.thisweek, self.area, res)
        return ""

    def get_product_url(self, product_name):
        res = self.product_kind.__dict__.get(product_name)
        if res:
            return util.join_slash(self.base_url, self.products, self.a, res)
        return ""

    def get_recursive_links(self, link, all_links: list):
        if link not in all_links:
            all_links.append(link)
            print(f"append: {link}")
            print("sleep 0.5...")
            time.sleep(0.5)
            line_up_links = self.get_line_up_links(link)
            for l in line_up_links:
                self.get_recursive_links(l, all_links)
            pager_links = self.get_pager_links(link)
            for l in pager_links:
                self.get_recursive_links(l, all_links)
        return

    def get_all_product_url(self) -> (list):
        return_list = []
        all_product_kind = self.product_kind.__dict__.keys()
        for product in all_product_kind:
            product_url = self.get_product_url(product)
            print(f"call: {product_url}")
            self.get_recursive_links(product_url, return_list)
        return return_list

    def get_line_up_links(self, product_url) -> (list):
        result_links = []
        soup = util.get_soup(product_url)
        line_up_elements = soup.find_all(class_="list_btn brn pbNested pbNestedWrapper")
        for ele in line_up_elements:
            url = util.join_slash(self.base_url, ele.find('a', href=True)['href'])
            result_links.append(url)
        return result_links

    def get_pager_links(self, product_url) -> (list):
        result_links = []
        soup = util.get_soup(product_url)
        pager_elements = soup.find_all(class_="pager_num")
        for ele in pager_elements:
            if ele not in result_links:
                a_tag = ele.find("a")
                if a_tag:
                    url = util.join_slash(self.base_url, a_tag.get('href'))
                    result_links.append(url)
        return result_links

    def get_area_items(self, area_name) -> (Items):
        url = self.get_area_url(area_name)
        soup = util.get_soup(url)
        items_div = self.get_items_tag_from_page(soup)
        return Items(items_div)


    def get_product_items(self, product_name) -> (Items):
        url = self.get_product_url(product_name)
        soup = util.get_soup(url)
        items_div = self.get_items_tag_from_page(soup)
        return Items(items_div)


    def get_all_product(self) -> (list):
        result = []
        all_product_url = self.get_all_product_url()
        for product_url in all_product_url:
            soup = util.get_soup(product_url)
            items_div = self.get_items_tag_from_page(soup)
            items_obj = Items(items_div)
            for item in items_obj.items:
                dic = item.to_dict()
                # prevent to insert same product.
                if dic['name'] not in [i['name'] for i in result]:
                    result.append(item.to_dict())
        return result



if __name__ == '__main__':
    # プロダクトは上記の取り方で取れると思う。
    util.solve_certificate_problem()
    # result = search("オムライス")
    # print(util.dict_to_json(result))
    # print(len(result))
    print("hello")
