from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin


def create_bank_send_msg(from_address: Address, to_address: Address, amount: int, denom: str) -> MsgSend:
    msg = MsgSend(
        from_address=str(from_address),
        to_address=str(to_address),
        amount=[Coin(amount=str(amount), denom=denom)]
    )

    return msg
