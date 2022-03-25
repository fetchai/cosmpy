#!/bin/bash

# this must match the key defined in testcase.py
# T0DO: generate a random private key in testcases.py, retrieve it's mnemonic, inject it in entrypoint.sh via docker env variable.
# TODO: requires cosmpy support for mnemonics and/or armored keys 
ROOT_MNEMONIC="bench horn trap exit shell gentle already already fish stumble tornado abuse orange tornado current stock stomach audit traffic client shell round bracket glory"
ROOT_KEY_NAME="validator"
MONIKER="cosmpy-node"
CHAIN_ID="cosmpy-testnet"
TOTAL_SUPPLY="1084639418096980660717398793"
STAKING_DENOM="atestfet"

fetchd init "${MONIKER}" --chain-id "${CHAIN_ID}"

# TODO: remove when we have https://github.com/cosmos/cosmos-sdk/pull/9776 
sed -i "s/\"stake\"/\"${STAKING_DENOM}\"/g" ~/.fetchd/config/genesis.json

echo "${ROOT_MNEMONIC}" | fetchd --keyring-backend test keys add "${ROOT_KEY_NAME}" --recover

fetchd --keyring-backend test keys list

fetchd --keyring-backend test add-genesis-account "${ROOT_KEY_NAME}" "${TOTAL_SUPPLY}${STAKING_DENOM}"
fetchd gentx "${ROOT_KEY_NAME}" "1000000000000000000${STAKING_DENOM}" --chain-id "${CHAIN_ID}" --keyring-backend test
fetchd collect-gentxs

fetchd start --rpc.laddr tcp://0.0.0.0:26657
