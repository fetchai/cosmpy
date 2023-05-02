# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from c4echain.cfedistributor import (
    query_pb2 as c4echain_dot_cfedistributor_dot_query__pb2,
)


class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Params = channel.unary_unary(
                '/chain4energy.c4echain.cfedistributor.Query/Params',
                request_serializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryParamsRequest.SerializeToString,
                response_deserializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryParamsResponse.FromString,
                )
        self.States = channel.unary_unary(
                '/chain4energy.c4echain.cfedistributor.Query/States',
                request_serializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryStatesRequest.SerializeToString,
                response_deserializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryStatesResponse.FromString,
                )


class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def Params(self, request, context):
        """Parameters queries the parameters of the module.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def States(self, request, context):
        """Queries a list of States items.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Params': grpc.unary_unary_rpc_method_handler(
                    servicer.Params,
                    request_deserializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryParamsRequest.FromString,
                    response_serializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryParamsResponse.SerializeToString,
            ),
            'States': grpc.unary_unary_rpc_method_handler(
                    servicer.States,
                    request_deserializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryStatesRequest.FromString,
                    response_serializer=c4echain_dot_cfedistributor_dot_query__pb2.QueryStatesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chain4energy.c4echain.cfedistributor.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def Params(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chain4energy.c4echain.cfedistributor.Query/Params',
            c4echain_dot_cfedistributor_dot_query__pb2.QueryParamsRequest.SerializeToString,
            c4echain_dot_cfedistributor_dot_query__pb2.QueryParamsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def States(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chain4energy.c4echain.cfedistributor.Query/States',
            c4echain_dot_cfedistributor_dot_query__pb2.QueryStatesRequest.SerializeToString,
            c4echain_dot_cfedistributor_dot_query__pb2.QueryStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
