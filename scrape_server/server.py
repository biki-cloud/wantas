import logging as log
import os
import sys
import time
from concurrent import futures
from pathlib import Path
from typing import List

import dataset
import grpc

sys.path.append(str(Path(__file__).parent.resolve()))
sys.path.append(str(Path(__file__).parent.parent.resolve()))
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))
from scrape_server import geo
from scrape_server import scrape_pb2
from scrape_server import scrape_pb2_grpc
from scrape_server.database import db
from scrape_server.mylog import log


def search(search_name: str, user_lat: float, user_lon: float) -> (List[dict]):
    """
    商品名を受け取り、データベースから名前が入った商品のリストを持ってくる。
    lat,lonから場所を検索し、商品が売られている場所のみをフィルターし、商品リストを返す。

    """

    log.info("invoked search function.")
    log.info(f"user lat: {user_lat}, user lon: {user_lon}")

    start = time.time()
    sqlite_db = dataset.connect("sqlite:///" + os.path.join("database", "db.sqlite"))
    product_and_store_info_list = []

    for dic in sqlite_db.query(f"SELECT * FROM products WHERE product_name LIKE '%{search_name}%'"):

        # suitedでproduct_region_listを文字列からリストに変換する
        product_info = db.suited(dic)

        # ユーザーの位置情報から一番近い店舗の情報を取得
        store_info: geo.StoreInfo = geo.get_most_near_store_info(user_lat, user_lon, product_info['store_table_name'])

        # 商品情報にユーザーから一番近い店舗情報を追記する
        product_info.update(store_info.__dict__)

        # 商品のregion_listと店舗情報から一番近くの店舗では商品が販売されているのか判断する
        if geo.is_contains(product_info):
            product_and_store_info_list.append(product_info)

    elapsed_time = time.time() - start
    log.info(f"search process time: {elapsed_time}")
    return product_and_store_info_list


def set_product_info(res: scrape_pb2.ScrapeManyTimesResponse, product_info: dict) -> None:
    """
    GRPCのレスポンスクラスに商品情報を登録する

    Args:
        res: GRPCのレスポンスクラス. これに商品情報を登録していく

                message ScrapeManyTimesResponse {
                  Result result = 1;
                  string message = 2;
                }

                message Result {
                  string productName = 1;
                  string productUrl = 2;
                  string productPrice = 3;
                  string productImgUrl = 4;
                  repeated string productRegionList = 5;
                  string storeName = 6;
                  string storeAddress = 7;
                  float storeLat = 8;
                  float storeLon = 9;
                }

        product_info: 商品情報が入っているdict

                {
                    "product_name": "str",
                    "product_url: "str",
                    "product_price": "str",
                    "product_img_url": "str",
                    "product_region_list": ["str",...],
                    "store_name": "str",
                    "store_address: "str",
                    "store_lat": float,
                    "store_lon": float
                }

    Returns:
        None

    """
    res.result.productName = product_info['product_name']
    res.result.productUrl = product_info['product_url']
    res.result.productPrice = product_info['product_price']
    res.result.productImgUrl = product_info['product_img_url']
    res.result.productRegionList.extend(product_info['product_region_list'])
    res.result.storeName = product_info['store_name']
    res.result.storeAddress = product_info['store_address']
    res.result.storeLat = product_info['store_lat']
    res.result.storeLon = product_info['store_lon']
    res.message = "yes"


def get_parameter_from_request(request) -> (
        str, str, str):
    """
    リクエストから商品名、ユーザーの位置情報を取り出し、返す

    Args:
        request: GoからのGRPCのリクエスト

    Returns:
        商品名、位置情報を返す

    """
    product_name = request.productName
    user_lat = request.userLat
    user_lon = request.userLon
    log.info(f"product_name: {product_name}")
    log.info(f"user_lat: {user_lat}")
    log.info(f"user_lon: {user_lon}")
    return product_name, user_lat, user_lon


class ScrapingServiceManyTimes(scrape_pb2_grpc.ScrapingServiceServicer):
    def __init__(self):
        pass

    # Goからのリクエスト
    def ScrapeManyTimes(self, request, context):
        log.info("Invoked ScrapeManyTimes from go client.")

        # GRPCのレスポンスを入れる用のリスト
        responses = []

        # リクエストからパラメータを取り出す。
        product_name, user_lat, user_lon = get_parameter_from_request(request)

        # ヒットした商品情報がdictで返され、リストで帰ってくる
        hit_product_info_list: List[dict] = search(product_name, user_lat, user_lon)
        results_len = len(hit_product_info_list)
        log.debug(f"scrape_results: {hit_product_info_list}")

        if hit_product_info_list:
            log.info(f"scraping results length is {results_len}")
            for product_info_dic in hit_product_info_list:
                log.info(product_info_dic)

                # GRPCのレスポンスクラスをインスタンス化
                res: scrape_pb2.ScrapeManyTimesResponse = scrape_pb2.ScrapeManyTimesResponse()

                # GRPCレスポンスにproduct_info_dicの値をセットする。
                set_product_info(res, product_info_dic)

                responses.append(res)

            for product_info_dic in responses:
                log.debug(f"send response to go client.")
                yield product_info_dic

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
