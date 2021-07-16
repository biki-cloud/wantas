import sys
from collections.abc import Callable
from bs4 import BeautifulSoup
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")

from scrape_server import util
from scrape_server.store import AbsStore

BASE_URL = "https://www.family.co.jp"
get_soup = util.get_soup_wrapper(BASE_URL) # 必ず必要

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


class FamilyMart(AbsStore):
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

    def get_kind_of_product_urls(self, get_soup: Callable[[str], BeautifulSoup]) -> (list):
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

    def get_products_url_in_kind_of_product_url(self, kind_of_product_url: str, get_soup: Callable[[str], BeautifulSoup]) -> (list):
        """商品種類ページの中の商品ページのurlを全て取得し、返す。

        Args:
            kind_of_product_url (str): 商品種類ページのurl
                example: https://www.family.co.jp/goods/omusubi.html

        Returns:
            list: 商品ページのurlを全て取得し、リストにして返す。
                example: https://www.family.co.jp/goods/omusubi/0416412.html
        """
        results = []
        soup = get_soup(kind_of_product_url)
        all_products_tag = soup.findAll('div', attrs={"ly-mod-layout-clm"})
        for product_tag in all_products_tag:
            product_url = product_tag.find('a', href=True)['href']
            results.append(product_url)
        return results

    def get_all_product(self) -> (list):
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
        results = []
        all_product_page_urls = []
        kind_of_product_urls = self.get_kind_of_product_urls(get_soup)
        for kind_of_product_url in kind_of_product_urls:
            print(f"kind_of_product_url: {kind_of_product_url}")
            if self.is_available_kind_of_product_url(kind_of_product_url):
                product_page_urls = self.get_products_url_in_kind_of_product_url(kind_of_product_url, get_soup)
                all_product_page_urls.extend(product_page_urls)

        # 途中で止まったらstart_idxを設定しなおすことで途中から始めることができる。
        for product_url in all_product_page_urls:
            print(f"product_url: {product_url}")
            # たまにスクレイピングできないurlが混ざっている。
            if BASE_URL in product_url and "?q=" not in product_url:
                product = Product(product_url)
                dic = product.to_dict()
                print(dic)
                # Prevent to insert same product.
                if dic['product_name'] not in [i['product_name'] for i in results]:
                    results.append(dic)
            print(len(results))
        return results



if __name__ == '__main__':
    fam = FamilyMart()
    results = fam.get_all_product()
    util.write_json_file("./product_familymart.json", results)

