# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import scrape_pb2 as scrape__pb2


class ScrapingServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ScrapeManyTimes = channel.unary_stream(
                '/hello.ScrapingService/ScrapeManyTimes',
                request_serializer=scrape__pb2.ScrapeManyTimesRequest.SerializeToString,
                response_deserializer=scrape__pb2.ScrapeManyTimesResponse.FromString,
                )


class ScrapingServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ScrapeManyTimes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ScrapingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ScrapeManyTimes': grpc.unary_stream_rpc_method_handler(
                    servicer.ScrapeManyTimes,
                    request_deserializer=scrape__pb2.ScrapeManyTimesRequest.FromString,
                    response_serializer=scrape__pb2.ScrapeManyTimesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hello.ScrapingService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ScrapingService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ScrapeManyTimes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/hello.ScrapingService/ScrapeManyTimes',
            scrape__pb2.ScrapeManyTimesRequest.SerializeToString,
            scrape__pb2.ScrapeManyTimesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
