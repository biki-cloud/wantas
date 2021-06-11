from concurrent import futures

import grpc
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import scrape_pb2
from scrape_server import scrape_pb2_grpc
from scrape_server import scrape_manager
from scrape_server.store import seveneleven


class ScrapingServiceManyTimes(scrape_pb2_grpc.ScrapingServiceServicer):
    def __init__(self):
        pass

    def ScrapeManyTimes(self, request, context):
        responses = []
        product_name = request.productName
        user_lat = request.userLat
        user_lon = request.userLon
        print(f"Received: {product_name}")
        scrape_results, store_lat, store_lon = scrape_manager.search(product_name, user_lat, user_lon)
        print("scrape_results")
        print(scrape_results)

        for result in scrape_results:
            res = scrape_pb2.ScrapeManyTimesResponse()
            res.storeLat = store_lat
            res.storeLon = store_lon
            res.product.name = result['name']
            res.product.url = result['url']
            res.product.price = result['price']
            res.product.region_list.extend(result['region_list'])
            responses.append(res)

        for r in responses:
            print(f"send: {r}")
            yield r


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scrape_pb2_grpc.add_ScrapingServiceServicer_to_server(ScrapingServiceManyTimes(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Starting gRPC sample server...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
