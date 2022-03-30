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
from dataclasses import dataclass


class NetworkConfigError(RuntimeError):
    pass


URL_PREFIXES = (
    "grpc+https",
    "grpc+http",
    "rest+https",
    "rest+http",
)


@dataclass
class NetworkConfig:
    chain_id: str
    fee_minimum_gas_price: int
    fee_denomination: str
    staking_denomination: str
    url: str

    def validate(self):
        if self.chain_id == "":
            raise NetworkConfigError("Chain id must be set")
        if self.url == "":
            raise NetworkConfigError("URL must be set")
        if not any(map(lambda x: self.url.startswith(x), URL_PREFIXES)):
            prefix_list = ", ".join(map(lambda x: f'"{x}"', URL_PREFIXES))
            raise NetworkConfigError(
                f"URL must start with one of the following prefixes: {prefix_list}"
            )

    @classmethod
    def capricorn_testnet(cls) -> "NetworkConfig":
        return NetworkConfig(
            chain_id="capricorn-1",
            url="grpc+https://grpc-capricorn.fetch.ai",
            fee_minimum_gas_price=5000000000,
            fee_denomination="atestfet",
            staking_denomination="atestfet",
        )

    @classmethod
    def fetch_mainnet(cls) -> "NetworkConfig":
        return NetworkConfig(
            chain_id="fetchhub-3",
            url="grpc+https://grpc-fetchhub.fetch.ai",
            fee_minimum_gas_price=5000000000,
            fee_denomination="afet",
            staking_denomination="afet",
        )

    @classmethod
    def latest_stable_testnet(cls) -> "NetworkConfig":
        return cls.capricorn_testnet()
