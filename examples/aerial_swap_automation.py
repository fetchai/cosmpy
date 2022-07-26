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
from time import sleep

from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet


def swap_native_for_cw20(swap_amount, pair_contract, wallet):
    tx = pair_contract.execute(
        {
            "swap": {
                "offer_asset": {
                    "info": {"native_token": {"denom": "atestfet"}},
                    "amount": str(swap_amount),
                }
            }
        },
        sender=wallet,
        funds=str(swap_amount) + "atestfet",
    )
    print("swapping native for cw20 tokens")
    tx.wait_to_complete()


def swap_cw20_for_native(swap_amount, pair_contract_address, token_contract, wallet):
    tx = token_contract.execute(
        {
            "send": {
                "contract": pair_contract_address,
                "amount": str(swap_amount),
                "msg": "eyJzd2FwIjp7fX0=",
            }
        },
        wallet,
    )
    print("swapping cw20 for native tokens")
    tx.wait_to_complete()


def _parse_commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "trading_wallet",
        type=int,
        nargs="?",
        default=1000000,
        help="initial atestfet balance to perform swaps using the liquidity pool",
    )
    parser.add_argument(
        "upper_bound",
        type=int,
        nargs="?",
        default=20.5,
        help="price upper bound that will trigger a swap from cw20 to native tokens",
    )
    parser.add_argument(
        "lower_bound",
        type=int,
        nargs="?",
        default=19.5,
        help="price lower bound that will trigger a swap from native to cw20 tokens",
    )
    parser.add_argument(
        "commission",
        type=int,
        nargs="?",
        default=0.003,
        help="LP commission, for terraswap the default is 0.3%",
    )
    parser.add_argument(
        "interval_time",
        type=int,
        nargs="?",
        default=5,
        help="interval time in seconds to query liquidity pool price",
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

    wallet_balance = ledger.query_bank_balance(wallet.address())

    while wallet_balance < (10**18):
        print("Providing wealth to wallet...")
        faucet_api.get_wealth(wallet.address())
        wallet_balance = ledger.query_bank_balance(wallet.address())

    # Define cw20, pair and liquidity token contracts
    token_contract_address = (
        "fetch1qr8ysysnfxmqzu7cu7cq7dsq5g2r0kvkg5e2wl2fnlkqss60hcjsxtljxl"
    )
    pair_contract_address = (
        "fetch1vgnx2d46uvyxrg9pc5mktkcvkp4uflyp3j86v68pq4jxdc8j4y0s6ulf2a"
    )

    token_contract = LedgerContract(
        path=None, client=ledger, address=token_contract_address
    )
    pair_contract = LedgerContract(
        path=None, client=ledger, address=pair_contract_address
    )

    # tokens in trading wallet (currency will vary [atestfet,cw20] )
    currency = "atestfet"
    tokens = args.trading_wallet

    # Swap thresholds
    upper_bound = args.upper_bound
    lower_bound = args.lower_bound

    # LP commission
    commission = args.commission

    # Wait time
    interval = args.interval_time

    while True:

        # Query LP status
        pool = pair_contract.query({"pool": {}})
        native_amount = int(pool["assets"][1]["amount"])
        cw20_amount = int(pool["assets"][0]["amount"])

        if currency == "atestfet":
            # Calculate received cw20 tokens if atestfet tokens are given to LP
            tokens_out = round(
                ((cw20_amount * tokens) / (native_amount + tokens)) * (1 - commission)
            )

            # Sell price of atestfet => give atestfet, get cw20
            sell_price = tokens / tokens_out
            print("atestfet sell price: ", sell_price)
            if sell_price <= lower_bound:
                swap_native_for_cw20(tokens, pair_contract, wallet)
                tokens = int(
                    token_contract.query(
                        {"balance": {"address": str(wallet.address())}}
                    )["balance"]
                )

                # Trading wallet currency changed to cw20
                currency = "CW20"
        else:
            # Calculate received atestfet tokens if cw20 tokens are given to LP
            tokens_out = round(
                ((native_amount * tokens) / (cw20_amount + tokens)) * (1 - commission)
            )

            # Buy price of atestfet => give cw20, get atestfet
            buy_price = tokens_out / tokens
            print("atestfet buy price: ", buy_price)
            if buy_price >= upper_bound:
                swap_cw20_for_native(
                    tokens, pair_contract_address, token_contract, wallet
                )
                tokens = tokens_out

                # Trading wallet currency changed to cw20
                currency = "atestfet"

        sleep(interval)


if __name__ == "__main__":
    main()
