from concurrent import futures

import grpc
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")

from scrape_server import scrape_pb2
from scrape_server import scrape_pb2_grpc
from scrape_server import scrape_manager
from scrape_server import seveneleven


class ScrapingServiceManyTimes(scrape_pb2_grpc.ScrapingServiceServicer):
    def __init__(self):
        pass

    def ScrapeManyTimes(self, request, context):
        reply_msgs = []
        product_name = request.productName
        user_lat = request.userLat
        user_lon = request.userLon
        print(f"Received: {product_name}")
        menu = ['rice', 'karei', 'sushi', 'salad', 'bread']
        price = ["145円", "222円", "555円", "22円", "800円"]
        scrape_results, store_lat, store_lon = scrape_manager.search(product_name, user_lat, user_lon)
        print(scrape_results)

        for result in scrape_results:
            scraping_result = scrape_pb2.ScrapeManyTimesResponse()
            scrape_results.storeLat = store_lat
            scrape_results.storeLon = store_lon
            scraping_result.product.name = result['name']
            scraping_result.product.url = result['url']
            scraping_result.product.price = result['price']
            scraping_result.product.region_list.extend(result['region_list'])
            reply_msgs.append(scraping_result)
        for i in reply_msgs:
            print(f"send: {i}")
            yield i


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scrape_pb2_grpc.add_ScrapingServiceServicer_to_server(ScrapingServiceManyTimes(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Starting gRPC sample server...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
