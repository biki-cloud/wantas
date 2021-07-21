from concurrent import futures

from typing import List
import grpc
import sys
import os
import logging as log
import dataset
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")
sys.path.append("/home/hibiki/wantas")
import time

from scrape_server import scrape_pb2
from scrape_server import scrape_pb2_grpc
from scrape_server import geo
from scrape_server.store import seveneleven
from scrape_server.mylog import log
from scrape_server.database import db


def search(search_name: str, user_lat: float, user_lon: float) -> (List[dict]):
    """
    商品名を受け取り、データベースから名前が入った商品のリストを持ってくる。
    lat,lonから場所を検索し、商品が売られている場所のみをフィルターし、商品リストを返す。
    """

    log.info("invoked search function.")
    log.info(f"user lat: {user_lat}, user lon: {user_lon}")

    start = time.time()
    db2 = dataset.connect("sqlite:///" + os.path.join("database", "db.sqlite"))
    product_and_store_info_list = []
    for dic in db2.query(f"SELECT * FROM products WHERE product_name LIKE '%{search_name}%'"):
        # suitedでproduct_region_listを文字列からリストに変換する
        product_info = db.suited(dic)
        # ユーザーの位置情報から一番近い店舗の情報を取得
        store_info: StoreInfo = geo.get_most_near_store_info(user_lat, user_lon, product_info['store_table_name'])
        # 商品情報にユーザーから一番近い店舗情報を追記する
        product_info.update(store_info.__dict__)
        # 商品のregion_listと店舗情報から一番近くの店舗では商品が販売されているのか判断する
        if geo.is_contains(product_info):
            product_and_store_info_list.append(product_info)
    elapsed_time = time.time() - start
    log.info(f"search process time: {elapsed_time}")
    return product_and_store_info_list


class ScrapingServiceManyTimes(scrape_pb2_grpc.ScrapingServiceServicer):
    def __init__(self):
        pass

    # Goからのリクエスト
    def ScrapeManyTimes(self, request, context):
        log.info("Invoked ScrapeManyTimes from go client.")
        responses = []
        # リクエストからパラメータを取り出す。
        product_name = request.productName
        user_lat = request.userLat
        user_lon = request.userLon
        log.info(f"product_name: {product_name}")
        log.info(f"user_lat: {user_lat}")
        log.info(f"user_lon: {user_lon}")

        scrape_results = search(product_name, user_lat, user_lon)
        results_len = len(scrape_results)
        log.debug(f"scrape_results: {scrape_results}")

        if scrape_results:
            log.info(f"scraping results length is {results_len}")
            for r in scrape_results:
                log.info(r)
                res = scrape_pb2.ScrapeManyTimesResponse()

                # レスポンスに値をセットする。
                res.result.productName = r['product_name']
                res.result.productUrl = r['product_url']
                res.result.productPrice = r['product_price']
                res.result.productImgUrl = r['product_img_url']
                res.result.productRegionList.extend(r['product_region_list'])
                res.result.storeName = r['store_name']
                res.result.storeAddress = r['store_address']
                res.result.storeLat = r['store_lat']
                res.result.storeLon = r['store_lon']
                res.message = "yes"

                responses.append(res)

            for r in responses:
                log.debug(f"send response to go client.")
                yield r
        else:
            # no result
            log.info("Scraping results is None.")
            res = scrape_pb2.ScrapeManyTimesResponse()
            res.result.productName = "none"
            res.message = "some message"
            yield res

def serve():
    log.info("Starting GRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scrape_pb2_grpc.add_ScrapingServiceServicer_to_server(ScrapingServiceManyTimes(), server)
    # 自分のアドレスのポート50051で待ち構える。後はclientからアクセスがくる。
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
