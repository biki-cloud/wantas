from concurrent import futures

import grpc

import scrape_pb2
import scrape_pb2_grpc
from scraping import do_scrape

class ScrapeServiceServer(scrape_pb2_grpc.ScrapeServiceServicer):
    def __init__(self):
        pass

    def Scrape(self, request: scrape_pb2.ScrapeRequest, context):
        name = request.name
        print("Scrape function is invoked from client")
        print(f"received name is {name}")
        dealer, price = do_scrape.test(name)
        print(f"send {dealer} {price} to client.")
        return scrape_pb2.ScrapeResponse(
            dealer=dealer,
            price=price,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scrape_pb2_grpc.add_ScrapeServiceServicer_to_server(ScrapeServiceServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Starting gRPC sample server...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
