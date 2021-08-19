# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from pycosm.protos.cosmos.slashing.v1beta1 import (
    tx_pb2 as cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2,
)


class MsgStub(object):
    """Msg defines the slashing Msg service."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Unjail = channel.unary_unary(
            "/cosmos.slashing.v1beta1.Msg/Unjail",
            request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2.MsgUnjail.SerializeToString,
            response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2.MsgUnjailResponse.FromString,
        )


class MsgServicer(object):
    """Msg defines the slashing Msg service."""

    def Unjail(self, request, context):
        """Unjail defines a method for unjailing a jailed validator, thus returning
        them into the bonded validator set, so they can begin receiving provisions
        and rewards again.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Unjail": grpc.unary_unary_rpc_method_handler(
            servicer.Unjail,
            request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2.MsgUnjail.FromString,
            response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2.MsgUnjailResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "cosmos.slashing.v1beta1.Msg", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Msg(object):
    """Msg defines the slashing Msg service."""

    @staticmethod
    def Unjail(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/cosmos.slashing.v1beta1.Msg/Unjail",
            cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2.MsgUnjail.SerializeToString,
            cosmos_dot_slashing_dot_v1beta1_dot_tx__pb2.MsgUnjailResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
