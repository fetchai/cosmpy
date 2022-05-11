# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Integration tests for basic transactions."""
import time
from collections import namedtuple
from typing import Optional, Union

import requests

from cosmpy.crypto.address import Address

_FETCHAI = "fetchai"
_FETCH = "fetch"
TESTNET_NAME = "testnet"
FETCHAI_TESTNET_FAUCET_URL = "https://faucet-dorado.fetch.ai"
DEFAULT_ADDRESS = "https://rest-dorado.fetch.ai:443"
DEFAULT_CURRENCY_DENOM = "atestfet"
DEFAULT_CHAIN_ID = "dorado-1"


CosmosFaucetStatus = namedtuple("CosmosFaucetStatus", ["tx_digest", "status"])


class TestNetFaucetApi:
    """Testnet faucet API."""

    IDENTIFIER = _FETCHAI
    TESTNET_NAME = TESTNET_NAME
    FAUCET_URL = FETCHAI_TESTNET_FAUCET_URL

    MAX_RETRY_ATTEMPTS = 10
    POLL_INTERVAL = 3
    FINAL_WAIT_INTERVAL = 5

    FAUCET_STATUS_PENDING = "pending"  # noqa: F841
    FAUCET_STATUS_PROCESSING = "processing"  # noqa: F841
    FAUCET_STATUS_COMPLETED = "complete"  # noqa: F841
    FAUCET_STATUS_FAILED = "failed"  # noqa: F841

    @classmethod
    def _claim_url(cls) -> str:
        return f"{cls.FAUCET_URL}/api/v3/claims"

    @classmethod
    def _status_uri(cls, uid: str) -> str:
        """
        Generates the status URI derived .

        :param uid: claim uid.
        :return: url string
        """
        return f"{cls._claim_url()}/{uid}"

    @classmethod
    def _try_create_faucet_claim(cls, address: str) -> Optional[str]:
        """
        Create a token faucet claim request

        :param address: the address to request funds
        :return: None on failure, otherwise the request uid
        """
        uri = cls._claim_url()
        response = requests.post(url=uri, json={"address": address})
        uid = None
        if response.status_code == 200:
            try:
                uid = response.json()["uuid"]
            except KeyError:  # pragma: nocover
                raise ValueError(
                    f"key `uid` not found in response_json={response.json()}"
                )

        return uid

    @classmethod
    def _try_check_faucet_claim(cls, uid: str) -> Optional[CosmosFaucetStatus]:
        """
        Check the status of a faucet request

        :param uid: The request uid to be checked
        :return: None on failure otherwise a CosmosFaucetStatus for the specified uid
        """
        response = requests.get(cls._status_uri(uid))
        if response.status_code != 200:  # pragma: nocover
            return None

        # parse the response
        data = response.json()
        tx_digest = None
        if "txStatus" in data["claim"]:
            tx_digest = data["claim"]["txStatus"]["hash"]

        return CosmosFaucetStatus(
            tx_digest=tx_digest,
            status=data["claim"]["status"],
        )

    @classmethod
    def get_wealth(cls, address: Union[Address, str]) -> None:
        """
        Get wealth from the faucet for the provided address.

        :param address: the address.
        :raises: RuntimeError of explicit faucet failures
        """
        address = str(address)
        uid = cls._try_create_faucet_claim(address)
        if uid is None:  # pragma: nocover
            raise RuntimeError("Unable to create faucet claim")

        retry_attempts = cls.MAX_RETRY_ATTEMPTS
        while retry_attempts > 0:
            retry_attempts -= 1

            # lookup status form the claim uid
            status = cls._try_check_faucet_claim(uid)
            if status is None:  # pragma: nocover
                raise RuntimeError("Failed to check faucet claim status")

            # if the status is complete
            if status.status == cls.FAUCET_STATUS_COMPLETED:
                break

            # if the status is failure
            if (
                status.status != cls.FAUCET_STATUS_PENDING
                and status.status != cls.FAUCET_STATUS_PROCESSING
            ):  # pragma: nocover
                raise RuntimeError(f"Failed to get wealth for {address}")

            # if the status is incomplete
            time.sleep(cls.POLL_INTERVAL)
        if retry_attempts == 0:
            raise ValueError("Faucet claim check timed out!")  # pragma: nocover
        # Wait to ensure that balance is increased on chain
        time.sleep(cls.FINAL_WAIT_INTERVAL)
