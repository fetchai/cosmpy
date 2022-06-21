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
import base64

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.tx_helpers import SubmittedTx
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey


def _wait_for_tx(operation: str, tx: SubmittedTx):
    print(f"Waiting for {operation} to complete... (tx: {tx.tx_hash})")
    tx.wait_to_complete()
    print(f"Waiting for {operation} to complete... done \n")


def main():

    # Choose any key with tokens available
    key = PrivateKey(
        b"@\xa95\x9a'\x972\xb88\x8b\x89\xccw0\xba\xed\x99m\xe9\x8f\xf0\xcf]\xb4\x93\xb13\xb9I\xdc\x96u"
    )
    wallet = LocalWallet(key)

    # Network configuration
    cfg = NetworkConfig(
        chain_id="dorado-1",
        url="grpc+https://grpc-dorado.fetch.ai:443",
        fee_minimum_gas_price=1000000000000,
        fee_denomination="atestfet",
        staking_denomination="atestfet",
    )

    ledger = LedgerClient(cfg)

    # Choose a path to any local file
    PATH = "any/path/to/a/local/file.any"

    # Define cw20, pair and liquidity token contracts
    token_contract_address = (
        "fetch1qr8ysysnfxmqzu7cu7cq7dsq5g2r0kvkg5e2wl2fnlkqss60hcjsxtljxl"
    )
    pair_contract_address = (
        "fetch1vgnx2d46uvyxrg9pc5mktkcvkp4uflyp3j86v68pq4jxdc8j4y0s6ulf2a"
    )
    liq_token_contract_address = (
        "fetch1alzhf9yhghud3qhucdjs895f3aek2egfq44qm0mfvahkv4jukx4qd0ltxx"
    )

    token_contract = LedgerContract(
        path=PATH, client=ledger, address=token_contract_address
    )
    pair_contract = LedgerContract(
        path=PATH, client=ledger, address=pair_contract_address
    )
    liq_token_contract = LedgerContract(
        path=PATH, client=ledger, address=liq_token_contract_address
    )

    print("Pool (initial state): ")
    print(pair_contract.query({"pool": {}}))

    # Swap atestfet for CW20 tokens
    swap_amount = "10000000"
    native_denom = "atestfet"

    print(f"Swapping {swap_amount + native_denom} for CW20 Tokens")

    tx = pair_contract.execute(
        {
            "swap": {
                "offer_asset": {
                    "info": {"native_token": {"denom": native_denom}},
                    "amount": swap_amount,
                }
            }
        },
        sender=wallet,
        funds=swap_amount + native_denom,
    )
    _wait_for_tx("swap", tx)

    print("Pool (after swap): ")
    print(pair_contract.query({"pool": {}}))

    # Increase Allowance
    native_liquidity_amount = "1000"

    tx = token_contract.execute(
        {
            "increase_allowance": {
                "spender": pair_contract_address,
                "amount": native_liquidity_amount,
                "expires": {"never": {}},
            }
        },
        wallet,
    )

    _wait_for_tx("increase allowance", tx)

    # Provide Liquidity
    cw20_liquidity_amount = "100"

    print(
        f"Providing {native_liquidity_amount + native_denom} and {cw20_liquidity_amount}CW20 tokens to Liquidity Pool"
    )

    tx = pair_contract.execute(
        {
            "provide_liquidity": {
                "assets": [
                    {
                        "info": {"token": {"contract_addr": token_contract_address}},
                        "amount": cw20_liquidity_amount,
                    },
                    {
                        "info": {"native_token": {"denom": native_denom}},
                        "amount": native_liquidity_amount,
                    },
                ]
            }
        },
        sender=wallet,
        funds=native_liquidity_amount + native_denom,
    )

    _wait_for_tx("provide liquidity", tx)

    print("Pool (after providing liquidity): ")
    print(pair_contract.query({"pool": {}}))

    # Withdraw Liquidity
    pair_withdraw_amount = "100"

    print(f"Withdrawing {pair_withdraw_amount} from pool's total share ")

    withdraw_msg = '{"withdraw_liquidity": {}}'
    withdraw_msg_bytes = withdraw_msg.encode("ascii")
    withdraw_msg_base64 = base64.b64encode(withdraw_msg_bytes)
    msg = str(withdraw_msg_base64)[2:-1]

    tx = liq_token_contract.execute(
        {
            "send": {
                "contract": pair_contract_address,
                "amount": pair_withdraw_amount,
                "msg": msg,
            }
        },
        sender=wallet,
    )

    _wait_for_tx("withdraw liquidity", tx)

    print("Pool (after withdrawing liquidity): ")
    print(pair_contract.query({"pool": {}}))


if __name__ == "__main__":
    main()
