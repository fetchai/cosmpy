# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
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

"""Network configurations."""

import warnings
from dataclasses import dataclass
from typing import Optional, Union


class NetworkConfigError(RuntimeError):
    """Network config error.

    :param RuntimeError: Runtime error
    """


URL_PREFIXES = (
    "grpc+https",
    "grpc+http",
    "rest+https",
    "rest+http",
)


@dataclass
class NetworkConfig:
    """Network configurations.

    :raises NetworkConfigError: Network config error
    :raises RuntimeError: Runtime error
    """

    chain_id: str
    fee_minimum_gas_price: Union[int, float]
    fee_denomination: str
    staking_denomination: str
    url: str
    faucet_url: Optional[str] = None

    def validate(self):
        """Validate the network configuration.

        :raises NetworkConfigError: Network config error
        """
        if self.chain_id == "":
            raise NetworkConfigError("Chain id must be set")
        if self.url == "":
            raise NetworkConfigError("URL must be set")
        if not any(
            map(
                lambda x: self.url.startswith(  # noqa: # pylint: disable=unnecessary-lambda
                    x
                ),
                URL_PREFIXES,
            )
        ):
            prefix_list = ", ".join(map(lambda x: f'"{x}"', URL_PREFIXES))
            raise NetworkConfigError(
                f"URL must start with one of the following prefixes: {prefix_list}"
            )

    @classmethod
    def chain4energy_veles_testnet(cls) -> "NetworkConfig":
        """Chain4energy veles testnet.

        :return: Network configuration
        """
        return NetworkConfig(
            chain_id="dorado-1",
            url="rest+https://lcd-testnet.c4e.io/",
            fee_minimum_gas_price=0.025,
            fee_denomination="uc4e",
            staking_denomination="uc4e",
            faucet_url=None,
        )

    @classmethod
    def chain4energy_alpha_testnet(cls):
        """Get the Chain4energy alpha testnet.

        :raises RuntimeError: No alpha testnet available
        """
        raise RuntimeError("No alpha testnet available")

    @classmethod
    def chain4energy_beta_testnet(cls):
        """Get the Chain4energy beta testnet.

        :raises RuntimeError: No beta testnet available
        """
        raise RuntimeError("No beta testnet available")

    @classmethod
    def chain4energy_stable_testnet(cls):
        """Get the Chain4energy stable testnet.

        :return: Chain4energy stable testnet. For now veles is Chain4energy stable testnet.
        """
        return cls.chain4energy_veles_testnet()

    @classmethod
    def chain4energy_mainnet(cls) -> "NetworkConfig":
        """Get the chain4energy mainnet configuration.

        :return: C4E mainnet configuration
        """
        return NetworkConfig(
            chain_id="perun-1",
            url="grpc+https://grpc.c4e.io",
            fee_minimum_gas_price=0.025,
            fee_denomination="uc4e",
            staking_denomination="uc4e",
            faucet_url=None,
        )

    @classmethod
    def latest_stable_testnet(cls) -> "NetworkConfig":
        """Get the latest stable testnet.

        :return: latest stable testnet
        """
        warnings.warn(
            "latest_stable_testnet is deprecated, use chain4energy_stable_testnet instead",
            DeprecationWarning,
        )
        return cls.chain4energy_stable_testnet()
