from concurrent import futures

import grpc

import scrape_pb2
import scrape_pb2_grpc
from scraping import do_scrape


class ScrapingServiceManyTimes(scrape_pb2_grpc.ScrapingServiceServicer):
    def __init__(self):
        pass

    def ScrapeManyTimes(self, request, context):
        reply_msgs = []
        product_name = request.productName
        print(f"Received: {product_name}")
        menu = ['rice', 'karei', 'sushi', 'salad', 'bread']
        price = ["145円", "222円", "555円", "22円", "800円"]
        scrape_results = do_scrape.search(product_name)
        print(scrape_results)

        for result in scrape_results:
            scraping_result = scrape_pb2.ScrapeManyTimesResponse()
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
