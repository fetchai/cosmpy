# Cosmpy

[![Checks amd Tests](https://github.com/fetchai/cosmpy/actions/workflows/workflow.yml/badge.svg)](https://github.com/fetchai/cosmpy/actions/workflows/workflow.yml)

A python library for interacting with cosmos based blockchain networks

## Installing

To install the project use:

    pip3 install cosmpy

## Getting started

Below is a simple example using the `SigningCosmWasmClient` and the `RestClient` channel.

    from cosmpy.clients.signing_cosmwasm_client import SigningCosmWasmClient
    from cosmpy.common.rest_client import RestClient

    channel = RestClient("http://<rest endpoint addres>")
    client = SigningCosmWasmClient(private_key, channel, "<chain id>")
    
    res = client.get_balance(client.address, "stake")
    print(f"Balance: {res.balance.amount} {res.balance.denom}")

## Extra Resources

* [Github Repo](https://github.com/fetchai/cosmpy)
* [Bug Reports](https://github.com/fetchai/cosmpy/issues)
* [Discussions](https://github.com/fetchai/cosmpy/discussions)
