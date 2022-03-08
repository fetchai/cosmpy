import argparse

from cosmpy.aerial import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.crypto.address import Address


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('contract_path', help='The path to the contract to upload')
    return parser.parse_args()


def main():
    private_key = PrivateKey('T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s=')
    address = Address(private_key)

    contract_path = '/home/ed/Code/Fetch/contracts-simple/artifacts/contracts_simple.wasm'

    ledger = LedgerClient(NetworkConfig.capricorn_testnet())

    contract = LedgerContract(contract_path, ledger, address=Address('fetch1a9up92q2xwxgdfvv7t0a0e3gkwqd7sfq5z5ajm'))
    contract.deploy({}, private_key)

    print(f'Contract deployed at: {contract.address}')

    result = contract.query({'get': {'owner': str(address)}})
    print('Initial state:', result)

    contract.execute({'set': {'value': 'foobar'}}, private_key)

    result = contract.query({'get': {'owner': str(address)}})
    print('State after set:', result)

    contract.execute({'clear': {}}, private_key)

    result = contract.query({'get': {'owner': str(address)}})
    print('State after clear:', result)


if __name__ == '__main__':
    main()
