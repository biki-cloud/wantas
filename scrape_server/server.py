from concurrent import futures

import grpc
import sys
import os
import logging as log
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import scrape_pb2
from scrape_server import scrape_pb2_grpc
from scrape_server import scrape_manager
from scrape_server.store import seveneleven
from scrape_server.mylog import log
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

        scrape_results, store_lat, store_lon = scrape_manager.search(product_name, user_lat, user_lon)
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
    print("start")
    serve()
