# Arcturus

[![Checks amd Tests](https://github.com/fetchai/arcturus/actions/workflows/workflow.yml/badge.svg)](https://github.com/fetchai/arcturus/actions/workflows/workflow.yml)

A python library for interacting with cosmos based blockchain networks

## Installing

To install the project use:

    pip3 install arcturus

## Getting started

Below is a simple example using the `SigningCosmWasmClient` and the `RestClient` channel.

    from arcturus.clients.signing_cosmwasm_client import SigningCosmWasmClient
    from arcturus.common.rest_client import RestClient

    channel = RestClient("http://<rest endpoint addres>")
    client = SigningCosmWasmClient(private_key, channel, "<chain id>")
    
    res = client.get_balance(client.address, "stake")
    print(f"Balance: {res.balance.amount} {res.balance.denom}")

## Extra Resources

* [Github Repo](https://github.com/fetchai/arcturus)
* [Bug Reports](https://github.com/fetchai/arcturus/issues)
* [Discussions](https://github.com/fetchai/arcturus/discussions)
