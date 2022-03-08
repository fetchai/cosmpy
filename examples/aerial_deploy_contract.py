import argparse

from cosmpy.aerial import LedgerClient, NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.crypto.address import Address


def _parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('contract_path', help='The path to the contract to upload')
    parser.add_argument('contract_address', nargs='?', type=Address,
                        help='The address of the contract is already deployed')
    return parser.parse_args()


def main():
    args = _parse_commandline()

    private_key = PrivateKey('T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s=')
    address = Address(private_key)

    ledger = LedgerClient(NetworkConfig.capricorn_testnet())

    contract = LedgerContract(args.contract_path, ledger, address=args.contract_address)
    contract.deploy({}, private_key)

    print(f'Contract deployed at: {contract.address}')

    result = contract.query({'get': {'owner': str(address)}})
    print('Initial state:', result)

    contract.execute({'set': {'value': 'foobar'}}, private_key).wait_to_complete()

    result = contract.query({'get': {'owner': str(address)}})
    print('State after set:', result)

    contract.execute({'clear': {}}, private_key).wait_to_complete()

    result = contract.query({'get': {'owner': str(address)}})
    print('State after clear:', result)


if __name__ == '__main__':
    main()
