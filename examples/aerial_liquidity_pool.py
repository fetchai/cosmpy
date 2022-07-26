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
import argparse
import base64

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "swap_amount",
        type=int,
        nargs="?",
        default=10000,
        help="atestfet swap amount to get some cw20 tokens on wallet's address",
    )
    parser.add_argument(
        "cw20_liquidity_amount",
        type=int,
        nargs="?",
        default=100,
        help="amount of cw20 tokens that will be provided to LP",
    )
    parser.add_argument(
        "native_liquidity_amount",
        type=int,
        nargs="?",
        default=2470,
        help="amount of atestfet tokens that will be provided to LP",
    )
    return parser.parse_args()


def main():
    args = _parse_commandline()

    # Define any wallet
    wallet = LocalWallet.generate()

    # Network configuration
    ledger = LedgerClient(NetworkConfig.latest_stable_testnet())

    # Add tokens to wallet
    faucet_api = FaucetApi(NetworkConfig.latest_stable_testnet())
    faucet_api.get_wealth(wallet.address())

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
        path=None, client=ledger, address=token_contract_address
    )
    pair_contract = LedgerContract(
        path=None, client=ledger, address=pair_contract_address
    )
    liq_token_contract = LedgerContract(
        path=None, client=ledger, address=liq_token_contract_address
    )

    print("Pool (initial state): ")
    print(pair_contract.query({"pool": {}}), "\n")

    # Swap atestfet for CW20 tokens
    swap_amount = str(args.swap_amount)
    native_denom = "atestfet"

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

    print(f"Swapping {swap_amount + native_denom} for CW20 Tokens...")
    tx.wait_to_complete()

    print("Pool (after swap): ")
    print(pair_contract.query({"pool": {}}), "\n")

    # To provide cw20 token to LP, increase your allowance first
    cw20_liquidity_amount = str(args.cw20_liquidity_amount)
    native_liquidity_amount = str(args.native_liquidity_amount)

    tx = token_contract.execute(
        {
            "increase_allowance": {
                "spender": pair_contract_address,
                "amount": cw20_liquidity_amount,
                "expires": {"never": {}},
            }
        },
        wallet,
    )

    print("Increasing Allowance...")
    tx.wait_to_complete()

    # Provide Liquidity
    # Liquidity should be added so that the slippage tolerance parameter isn't exceeded

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
                ],
                "slippage_tolerance": "0.1",
            }
        },
        sender=wallet,
        funds=native_liquidity_amount + native_denom,
    )

    print(
        f"Providing {native_liquidity_amount + native_denom} and {cw20_liquidity_amount}CW20 tokens to Liquidity Pool..."
    )
    tx.wait_to_complete()

    print("Pool (after providing liquidity): ")
    print(pair_contract.query({"pool": {}}), "\n")

    # Withdraw Liquidity
    LP_token_balance = liq_token_contract.query(
        {"balance": {"address": str(wallet.address())}}
    )["balance"]

    withdraw_msg = '{"withdraw_liquidity": {}}'
    withdraw_msg_bytes = withdraw_msg.encode("ascii")
    withdraw_msg_base64 = base64.b64encode(withdraw_msg_bytes)
    msg = str(withdraw_msg_base64)[2:-1]

    tx = liq_token_contract.execute(
        {
            "send": {
                "contract": pair_contract_address,
                "amount": LP_token_balance,
                "msg": msg,
            }
        },
        sender=wallet,
    )

    print(f"Withdrawing {LP_token_balance} from pool's total share...")
    tx.wait_to_complete()

    print("Pool (after withdrawing liquidity): ")
    print(pair_contract.query({"pool": {}}), "\n")


if __name__ == "__main__":
    main()
