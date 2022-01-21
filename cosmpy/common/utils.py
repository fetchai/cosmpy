import time
from typing import List, Union

import requests
from grpc._channel import Channel

from cosmpy.bank.rest_client import BankRestClient
from cosmpy.common.loggers import get_logger
from cosmpy.common.rest_client import RestClient
from cosmpy.crypto.address import Address
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from cosmpy.protos.cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankGrpcClient

_logger = get_logger(__name__)


def get_balance(
    channel: Union[Channel, RestClient], address: Address, denom: str
) -> int:
    """
    Get balance of specific account and denom

    :param channel: Rest or Grpc channel
    :param address: Address
    :param denom: Denomination

    :return: amount
    """

    if isinstance(channel, Channel):
        bank_client: Union[BankRestClient, BankGrpcClient] = BankGrpcClient(channel)
    elif isinstance(channel, RestClient):
        bank_client = BankRestClient(channel)
    else:
        raise RuntimeError(
            f"Unsupported channel type {type(channel)}"
        )  # pragma: no cover

    res = bank_client.Balance(QueryBalanceRequest(address=str(address), denom=denom))
    return int(res.balance.amount)


def refill_wealth_from_faucet(
    channel: Union[Channel, RestClient],
    faucet_url: str,
    addresses: List[Address],
    denom: str,
):
    """
    Uses faucet api to refill balance of addresses

    :param channel: Rest or Grpc channel
    :param faucet_url: Faucet URL
    :param addresses: List of addresses to be refilled
    :param denom: Denomination

    :raises RuntimeError: if getting funds fails.
    """

    faucet_retry_interval = 10

    for address in addresses:
        attempts_allowed = 10

        min_amount_required = 500000000

        # Retry in case of network issues
        while attempts_allowed > 0:
            try:
                attempts_allowed -= 1
                balance = get_balance(channel, address, denom)

                if balance < min_amount_required:
                    # Send faucet request
                    response = requests.post(
                        f"{faucet_url}/api/v3/claims",
                        json={"address": str(address)},
                    )

                    if response.status_code != 200:
                        _logger.exception(
                            f"Failed to refill the balance from faucet, retry in {faucet_retry_interval} seconds: {str(response)}"
                        )

                    # Wait for wealth to be refilled
                    time.sleep(faucet_retry_interval)
                    continue
                break
            except Exception as e:  # pylint: disable=W0703
                _logger.exception(
                    f"Failed to refill the balance from faucet, retry in {faucet_retry_interval} second: {e} ({type(e)})"
                )
                time.sleep(faucet_retry_interval)
                continue
