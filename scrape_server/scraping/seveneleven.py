import time
from typing import List
from collections import Counter

import bs4

import scrape_util as util


class ProductKinds:
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


class SevenEleven:
    def __init__(self):
        self.base_url = "https://www.sej.co.jp"
        self.products = "products"
        self.a = "a"
        self.area = "area"
        self.product_kind = ProductKinds()
        self.areas = Area()

    @classmethod
    def get_items_tag_from_page(cls, soup) -> bs4.element.ResultSet:
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

    def get_all_product_url(self) -> list:
        return_list = []
        all_product_kind = self.product_kind.__dict__.keys()
        for product in all_product_kind:
            product_url = self.get_product_url(product)
            print(f"call: {product_url}")
            self.get_recursive_links(product_url, return_list)
        return return_list

    def get_line_up_links(self, product_url) -> list:
        result_links = []
        soup = util.get_soup(product_url)
        line_up_elements = soup.find_all(class_="list_btn brn pbNested pbNestedWrapper")
        for ele in line_up_elements:
            url = util.join_slash(self.base_url, ele.find('a', href=True)['href'])
            result_links.append(url)
        return result_links

    def get_pager_links(self, product_url) -> list:
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


class Items:
    def __init__(self, items_div: bs4.element.ResultSet):
        self.items_div: List[bs4.element.Tag] = [i for i in items_div]
        self.items = [Item(item_tag) for item_tag in self.items_div]


class Item:
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

    def to_dict(self) -> dict:
        return {
            "name": self.title,
            "url": self.url,
            "price": self.price,
            "region_list": self.region_list
        }

    def get_title(self) -> (str, str):
        title_tag = self.item.find('div', attrs={"class", "item_ttl"})
        title = title_tag.string
        url = title_tag.find('a', href=True)['href']
        seven = SevenEleven()
        url = util.join_slash(seven.base_url, url)
        return title

    def get_url(self) -> str:
        title_tag = self.item.find('div', attrs={"class", "item_ttl"})
        url = title_tag.find('a', href=True)['href']
        seven = SevenEleven()
        url = util.join_slash(seven.base_url, url)
        return url

    def get_price(self) -> str:
        price_tag = self.item.find('div', attrs={"class", "item_price"})
        return price_tag.string

    def get_region(self) -> list:
        region_tag = self.item.find('div', attrs={"class", "item_region"})
        p_tag = region_tag.find('p')
        region_str = p_tag.getText()
        deleted_str = region_str.replace("販売地域：", "")
        return deleted_str.split("、")

    def display_properties(self):
        for k, v in self.to_dict.items():
            print(f"{k}: {v}")


def get_area_items(area_name, seven: SevenEleven) -> Items:
    url = seven.get_area_url(area_name)
    soup = util.get_soup(url)
    items_div = seven.get_items_tag_from_page(soup)
    return Items(items_div)


def get_product_items(product_name, seven: SevenEleven) -> Items:
    url = seven.get_product_url(product_name)
    soup = util.get_soup(url)
    items_div = seven.get_items_tag_from_page(soup)
    return Items(items_div)


def items_to_database(database, items_obj: Items):
    for item in items_obj.items:
        database.append(
            {
                "name": item.title,
                "url": item.url,
                "price": item.price,
                "region": item.region_list
            }
        )


def search_from_database(database, search_name):
    result = []
    for record in database:
        if search_name in record['name']:
            result.append(record)
    return result


def get_all_product(seven: SevenEleven):
    result = []
    all_product_url = seven.get_all_product_url()
    for product_url in all_product_url:
        soup = util.get_soup(product_url)
        items_div = seven.get_items_tag_from_page(soup)
        items_obj = Items(items_div)
        for item in items_obj.items:
            dic = item.to_dict()
            if dic['name'] not in [i['name'] for i in result]:
                result.append(item.to_dict())
    return result

def research_to_database(database_path, seven: SevenEleven):
    database: List[dict] = get_all_product(seven)
    util.write_json_file(database_path, database)

def read_database(database_path):
    return util.read_json_file(database_path)

def search(search_name: str):
    seven = SevenEleven()

    database_path = "database.json"

    database = read_database(database_path)

    result = search_from_database(database, search_name)
    # print(util.dict_to_json(result))
    print("***** result *****")
    print(f"total: {len(database)}")
    print(f"hits:  {len(result)}")
    print("******************")
    return result


if __name__ == '__main__':
    # プロダクトは上記の取り方で取れると思う。
    util.solve_certificate_problem()
    result = search("オムライス")
    print(util.dict_to_json(result))
    print(len(result))
