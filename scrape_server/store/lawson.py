import os
import sys
from typing import List

import bs4

from scrape_server import util

BASE_URL = "https://www.lawson.co.jp"
get_soup = util.get_soup_wrapper(BASE_URL)  # 必ず必要


class Product:
    """商品ページurlを受け取り、名前、値段などを格納するクラス

    Args:
        product_info_soup: 商品情報の入ったタグ
            例 -> <li>
                <p class="img"><a href="/recommend/original/detail/1430800_1996.html"><img alt="おにからセット(シーチキンマヨネーズ・日高昆布)" height="169" src="/recommend/original/detail/img/l650329.jpg" width="220"/></a></p>
                <p class="ttl">おにからセット(シーチキンマヨネーズ・日高昆布)</p>
                <p>452kcal</p>
                <p class="price"><span>298円</span><span>(税込)</span></p>
                <p class="smalltxt" style="padding-top:5px;">※近畿・中四国地域のローソンではお取り扱いしておりません。</p>
                </li>a
    """

    def __init__(self, product_info_soup: bs4.element.Tag):
        self.product_info_soup = product_info_soup
        self.url = self.get_url()
        self.name = self.get_name()
        self.price = self.get_price()
        self.img_url = self.get_img_url()
        self.region_list = self.get_region_list()
        self.store_table_name = "store_lawson"

    def get_url(self):
        a_tag = self.product_info_soup.find('a')
        return util.url_join(BASE_URL, a_tag['href'])

    def get_name(self):
        name_tag = self.product_info_soup.find('p', attrs={"class", "ttl"})
        return name_tag.get_text()

    def get_price(self):
        price_tag = self.product_info_soup.find('p', attrs={"class", "price"})
        return price_tag.text

    def get_img_url(self):
        img_tag = self.product_info_soup.find('img')
        return util.url_join(BASE_URL, img_tag['src'])

    def get_region_list(self):
        region_msg_tag = self.product_info_soup.find('p', attrs={"class", "smalltxt"})
        try:  # textがない場合がある
            region_msg = region_msg_tag.text
        except AttributeError:
            return ["全国"]
        if "地域" not in region_msg:
            return ["全国"]
        if "※" in region_msg:
            region_msg = region_msg[region_msg.index("※"):]
        region_str = region_msg[1:region_msg.index("地域")]
        region_list = region_str.split("・")
        # ここでのregionはその地域意外で販売なので頭に!をつける。
        return ["!" + region for region in region_list]

    def to_dict(self) -> (dict):
        return {
            "product_name": self.name,
            "product_url": self.url,
            "product_price": self.price,
            "product_region_list": self.region_list,
            "product_img_url": self.img_url,
            "store_table_name": self.store_table_name
        }


class Lawson:
    def __init__(self):
        self.base_url = "https://www.lawson.co.jp"

    def get_all_type_of_product_urls(self) -> (list):
        """ローソンのホームページから商品の種類のページURLのリストを返す。

        Returns:
            list: 商品の種類のページURLのリストを返す。
                リストの中の一つの例 -> https://www.lawson.co.jp/recommend/original/rice/
        """
        results = []
        soup = get_soup(self.base_url)
        li_tags = soup.findAll('li')
        for li_tag in li_tags:
            if "/recommend/original" in str(li_tag):
                results.append(util.url_join(self.base_url, li_tag.find('a', href=True)['href']))
        return results

    def get_product_infos_from_type_of_product_url(self, type_of_product_url) -> (List[bs4.element.Tag]):
        """ 商品がリストで掲載されているページから商品情報のタグをリストで返す。

        Args:
            type_of_product_url (str): 商品がリストで掲載されているページのURL
                例 -> https://www.lawson.co.jp/recommend/original/rice/

        Returns:
            list: 商品情報が入ったタグをリストにして返す。
                リストの中の一つの例 -> <li>
                                    <p class="img"><a href="/recommend/original/detail/1430800_1996.html"><img alt="おにからセット(シーチキンマヨネーズ・日高昆布)" height="169" src="/recommend/original/detail/img/l650329.jpg" width="220"/></a></p>
                                    <p class="ttl">おにからセット(シーチキンマヨネーズ・日高昆布)</p>
                                    <p>452kcal</p>
                                    <p class="price"><span>298円</span><span>(税込)</span></p>
                                    <p class="smalltxt" style="padding-top:5px;">※近畿・中四国地域のローソンではお取り扱いしておりません。</p>
                                    </li>
        """
        soup = get_soup(type_of_product_url)
        all_product_info_tag = soup.find('ul', attrs={"class", "col-4 heightLineParent"})
        product_info_tags = all_product_info_tag.findAll("li")
        return product_info_tags

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
        results = []
        progress_file_path = f"{json_path}_progress.json"
        if os.path.exists(progress_file_path):
            progress_dic = util.read_json_file(progress_file_path)
            type_of_product_url_idx = progress_dic['type_of_product_url_idx']
            product_info_idx = progress_dic['product_info_idx']
        else:
            type_of_product_url_idx = 0
            product_info_idx = 0
        get_soup = util.get_soup_wrapper(BASE_URL)  # 必ず必要
        all_type_of_product_urls = self.get_all_type_of_product_urls()
        for i, type_of_product_url in enumerate(all_type_of_product_urls[type_of_product_url_idx:],
                                                start=type_of_product_url_idx):
            product_infos = self.get_product_infos_from_type_of_product_url(type_of_product_url)
            for j, product_info in enumerate(product_infos[product_info_idx:], start=product_info_idx):
                # 進捗状況を書き込む
                d = {"type_of_product_url_idx": i, "product_info_idx": j}
                util.write_json_file(progress_file_path, d)
                product_dic = Product(product_info).to_dict()
                if product_dic['product_name'] not in [i['product_name'] for i in results]:
                    # リストに商品情報を追加
                    results.append(product_dic)
                    # リストを書き込む
                    util.write_json_file(json_path, results)

            product_info_idx = 0
        os.remove(progress_file_path)


if __name__ == '__main__':
    lawson = Lawson()
    lawson.scraping_to_json_file(sys.argv[1])
