import sys
from collections.abc import Callable
from bs4 import BeautifulSoup
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")
sys.path.append("/home/hibiki/wantas")
import os

from scrape_server import util
from scrape_server.store import AbsStore

BASE_URL = "https://www.family.co.jp"
get_soup = util.get_soup_wrapper(BASE_URL) # 必ず必要

PLAN_TO_SCRAPE_PRODUCT_NAME_LIST = []

class Product:
    """商品ページurlを受け取り、名前、値段などを格納するクラス
    """
    def __init__(self, page_url: str):
        self.url = page_url
        self.page_soup = get_soup(self.url)
        self.name = self.get_product_name()
        self.price = self.get_product_price()
        self.img_url = self.get_img_url()
        self.region_list = self.get_region_list()
        self.store_table_name = "store_familymart"

    def to_dict(self) -> (dict):
        return {
            "product_name": self.name,
            "product_url": self.url,
            "product_price": self.price,
            "product_region_list": self.region_list,
            "product_img_url": self.img_url,
            "store_table_name": self.store_table_name
        }

    def get_product_name(self) -> (str):
        """商品ページから商品名を返す。
        """
        product_name_tag = self.page_soup.find('h1', attrs={"class", "ly-mod-ttl-main"})
        return product_name_tag.get_text()

    def get_product_price(self) -> (str):
        """商品ページから値段を返す。
        """
        product_price_tag = self.page_soup.find('span', attrs={"class", "ly-kakaku-usual"})
        if product_price_tag is None:
            # 価格が割引になっている場合
            product_price_tag = self.page_soup.find('span', attrs={"class", "ly-kakaku-after"})
            product_price_tax_tag = self.page_soup.find('span', attrs={"class", "ly-kakaku-zei"})
            price = product_price_tag.get_text() + product_price_tax_tag.get_text()
            # 改行やスペースが多数含まれるので削除
            return price.replace(" ", "").replace("\n", "").replace("\t", "")
        price = product_price_tag.get_text()
        return price.replace(" ", "").replace("\n", "").replace("\t", "")

    def get_region_list(self) -> (list):
        """商品ページから販売している地域のリストを返す。
        """
        results = []
        region_tags = self.page_soup.findAll('p', attrs={"class", "ly-mod-tag"})
        for region_tag in region_tags:
            txt = region_tag.get_text()
            if txt != "発売地域" and txt != "一般":
                if txt == "中国・四国":
                    results.append("中国")
                    results.append("四国")
                else:
                    results.append(txt)
        return results

    def get_img_url(self) -> (str):
        """商品ページから商品の画像urlを返す。
        """
        img_div_tag = self.page_soup.find('div', attrs={"class", "js-mainimage-size"})
        img_tag = img_div_tag.find('img')
        return util.url_join(BASE_URL,img_tag['src'])


class FamilyMart:
    def __init__(self):
        pass

    def is_available_kind_of_product_url(self, url: str) -> (list):
        """https://www.family.co.jp/goods.htmlのページの中に商品の種類が掲載されている
        その中でスクレイピングできる商品種類のリンクだったらTrue
        """
        base_url = "https://www.family.co.jp/goods/"
        html_list = [
            "omusubi.html",
            "obento.html",
            "sushi.html"
            "sandwich.html",
            "bread.html",
            "noodle.html",
            "pasta.html",
            "salad.html",
            "sidedishes.html",
            "deli.html",
            "chilleddaily.html",
            "friedfoods.html",
            "chukaman.html",
            "oden.html",
            "dessert.html",
            "wagashi.html",
            "baked_sweets.html",
            "cafe.html",
            "okasanshokudo.html",
            "famicolle.html",
            "processed_foods.html",
            "snack.html",
            "drink.html",
            "alcohol.html",
            "frozen_foods.html",
            "ice.html",
            "daily_necessities.html",
            "cw.html",
            "books.html",
            "disc.html",
            "charakuji.html",
            "cosmetics.html",
        ]
        available_urls = []
        for html in html_list:
            available_urls.append(base_url + html)
        return url in available_urls

    def get_kind_of_products_listed_page(self) -> (str):
        """商品の種類がリストされているページのurlを取得する
        """
        return util.url_join(BASE_URL, "goods.html")

    def get_kind_of_product_urls(self, get_soup) -> (list):
        """商品の種類がリストされているページの中の商品の種類のページurlをリストにして返す。

        Returns:
            list: 種類ページのurlリストを返す。
            example: https://www.family.co.jp/goods/omusubi.html
        """
        results = []
        url = self.get_kind_of_products_listed_page()
        soup = get_soup(url)
        kind_of_product_tags = soup.findAll('div', attrs={"ly-mod-layout-clm"})
        for kind_of_product_tag in kind_of_product_tags:
            kind_of_product_url = kind_of_product_tag.find('a', href=True)['href']
            results.append(kind_of_product_url)
        return results

    def get_products_url_in_kind_of_product_url(self, kind_of_product_url: str, get_soup) -> (list):
        """商品種類ページの中の商品ページのurlを全て取得し、返す。

        Args:
            kind_of_product_url (str): 商品種類ページのurl
                example: https://www.family.co.jp/goods/omusubi.html

        Returns:
            list: 商品ページのurlを全て取得し、リストにして返す。
                example: https://www.family.co.jp/goods/omusubi/0416412.html
        """
        product_urls = []
        soup = get_soup(kind_of_product_url)
        all_products_tags = soup.findAll('div', attrs={"ly-mod-infoset4 js-imgbox-size-rel"})
        for product_tag in all_products_tags:
            product_name = product_tag.find('p', attrs={"ly-mod-infoset4-name"}).get_text()
            # 商品の名前が被る場合があるため下の処理をしている。被った場合は余分にスクレイピングし、時間がかかるので
            if product_name not in PLAN_TO_SCRAPE_PRODUCT_NAME_LIST:
                PLAN_TO_SCRAPE_PRODUCT_NAME_LIST.append(product_name)
                product_info_url = product_tag.find('a', href=True)['href']
                product_urls.append(product_info_url)
        return product_urls

    def scraping_to_json_file(self, json_path: str) -> (list):
        """全ての商品情報を取得し、リストで返す。

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
        all_product_info_list = []
        all_product_page_urls = []
        kind_of_product_urls = self.get_kind_of_product_urls(get_soup)
        for kind_of_product_url in kind_of_product_urls:
            if self.is_available_kind_of_product_url(kind_of_product_url):
                product_page_urls = self.get_products_url_in_kind_of_product_url(kind_of_product_url, get_soup)
                all_product_page_urls.extend(product_page_urls)

        progress_file_path = f"{json_path}_progress.json"
        print(f"SCRAPE_PRODUCTS length: {len(PLAN_TO_SCRAPE_PRODUCT_NAME_LIST)}") # 1700
        print(f"all_product_page_urls: {len(all_product_page_urls)}")
        if os.path.exists(progress_file_path):
            progress_dic = util.read_json_file(progress_file_path)
            start_idx = progress_dic['start_idx']
        else:
            start_idx = 0
        for i, product_url in enumerate(all_product_page_urls[start_idx:], start=start_idx):
            # たまにスクレイピングできないurlが混ざっている。
            if BASE_URL in product_url and "?q=" not in product_url:
                # 進捗状況を書き込む
                d = {"start_idx": i}
                util.write_json_file(progress_file_path, d)
                product = Product(product_url)
                product_dic = product.to_dict()
                # 同じ名前の情報を登録するのを防ぐ
                if product_dic['product_name'] not in [i['product_name'] for i in all_product_info_list]:
                    # リストに商品情報を追加
                    all_product_info_list.append(product_dic)
                    # リストに書き込む
                    util.write_json_file(json_path, all_product_info_list)
        os.remove(progress_file_path)


if __name__ == '__main__':
    fam = FamilyMart()
    fam.scraping_to_json_file(sys.argv[1])
