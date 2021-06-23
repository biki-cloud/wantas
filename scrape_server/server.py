from concurrent import futures

import grpc
import sys
import os
import logging as log
import dataset
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import scrape_pb2
from scrape_server import scrape_pb2_grpc
from scrape_server import geo
from scrape_server.store import seveneleven
from scrape_server.mylog import log
from scrape_server.database import db

def search(search_name: str, user_lat: float, user_lon: float) -> (list, float, float):
    """
    商品名を受け取り、スクレイプし名前が入った商品のリストを持ってくる。
    lat,lonから場所を検索し、商品が売られている場所のみをフィルターし、商品リストを返す。
    """

    log.info("invoked search function.")
    log.info(f"user lat: {user_lat}, user lon: {user_lon}")

    # scrape_serverディレクトリで実行する必要がある。
    db2 = dataset.connect("sqlite:///" + os.path.join("database", "db.sqlite"))
    # db2 = dataset.connect(os.path.join("database", "db.sqlite"))
    product_table = db2["products"]
    result = db.search(product_table, "name", search_name)
    result = db.suited_products_table(result)

    # ユーザーから一番近い店舗の情報を取得
    store_info: StoreInfo = geo.get_most_near_store_info(user_lat, user_lon)
    log.info("got most near store information")
    log.info(store_info.__dict__)

    # ユーザーに一番近い店舗がある地域のみでフィルターする。
    filtered_results = []
    for ele in result:
        if geo.is_contains(ele['region_list'], store_info):
            filtered_results.append(ele)
    result = filtered_results

    log.info("return from search funcion.")
    log.info(f"result: {result}")
    log.info(f"most near store lat: {store_info.lat}, store lon: {store_info.lon}")
    return result, store_info.lat, store_info.lon


class ScrapingServiceManyTimes(scrape_pb2_grpc.ScrapingServiceServicer):
    def __init__(self):
        pass

    def ScrapeManyTimes(self, request, context):
        log.info("Invoked ScrapeManyTimes.")
        responses = []
        product_name = request.productName
        user_lat = request.userLat
        user_lon = request.userLon
        log.info(f"product_name: {product_name}")
        log.info(f"user_lat: {user_lat}")
        log.info(f"user_lon: {user_lon}")

        scrape_results, store_lat, store_lon = search(product_name, user_lat, user_lon)
        results_len = len(scrape_results)
        log.info(f"scrape_results: {scrape_results}")

        if scrape_results:
            log.info(f"scraping results length is {results_len}")
            for result in scrape_results:
                res = scrape_pb2.ScrapeManyTimesResponse()
                res.storeLat = float(store_lat)
                res.storeLon = float(store_lon)
                res.product.name = result['name']
                res.product.url = result['url']
                res.product.price = result['price']
                res.product.region_list.extend(result['region_list'])
                responses.append(res)

            for r in responses:
                log.debug(f"send response to go client.")
                yield r
        else:
            # no result
            res = scrape_pb2.ScrapeManyTimesResponse()
            log.info("Scraping results is None.")
            res.storeLat = 0.0
            res.storeLon = 0.0
            res.product.name = "none"
            res.product.url = "none"
            res.product.price = "none"
            res.product.region_list.extend(["none"])
            log.info(f"send response to go client.")
            yield res

def serve():
    log.info("Starting GRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scrape_pb2_grpc.add_ScrapingServiceServicer_to_server(ScrapingServiceManyTimes(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
