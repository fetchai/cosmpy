from cosmpy.aerial import LedgerClient, NetworkConfig
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey


def main():
    alice_private_key = PrivateKey('T7w1yHq1QIcQiSqV27YSwk+i1i+Y4JMKhkpawCQIh6s=')
    bob_private_key = PrivateKey('CI5AZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV8=')

    alice_address = Address(alice_private_key)
    bob_address = Address(bob_private_key)

    ledger = LedgerClient(NetworkConfig.capricorn_testnet())

    print(f'Alice Address: {alice_address} Balance: {ledger.query_bank_balance(alice_address)}')
    print(f'Bob   Address: {bob_address} Balance: {ledger.query_bank_balance(bob_address)}')


if __name__ == '__main__':
    main()
