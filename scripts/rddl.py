import argparse
from cosmpy.aerial.client import LedgerClient, NetworkConfig

def query_validator_balances(network: str, address: str):
    """
    Queries the bank balances of a validator on a specified network.

    Args:
        network: The network to connect to ('localhost', 'testnet', or 'mainnet').
        validator_address: The address of the validator.
    """
    if network == 'localhost':
        config = NetworkConfig.rddl_localhost()
        if not address or address == "":
          address = "plmnt1ch26lmn6gwcyny9lfq9cyet76ylav9fmr9frm9"
    elif network == 'testnet':
        config = NetworkConfig.rddl_testnet()
        if not address or address == "":
            address = "plmnt168z8fyyzap0nw75d4atv9ucr2ye60d57dzlzaf"
    elif network == 'mainnet':
        config = NetworkConfig.rddl_mainnet()
        if not address or address == "":
          address = "plmnt12t05rud2q3n9plscehf3s0yyan42pp8asf9wu4"
    else:
        print(f"Error: Invalid network '{network}'. Must be 'localhost', 'testnet', or 'mainnet'.")
        return
    if not address or address == "":
        print(f"Error: Address is invalid '{address}'.")
        return

    try:
      # connect to rddl network using default parameters
        ledger_client = LedgerClient(config)
        balances = ledger_client.query_bank_all_balances(address)

        print(f"Balances for address '{address}' on {network}:")
        for coin in balances:
            print(f'{coin.amount} {coin.denom}')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the bank balances of an account on a rddl network.")
    parser.add_argument("address", help="The address to query.", default="plmnt1ch26lmn6gwcyny9lfq9cyet76ylav9fmr9frm9")
    parser.add_argument(
        "--network",
        default="localhost",
        choices=['localhost', 'testnet', 'mainnet'],
        help="The network to connect to (default: mainnet)",
    )
    args = parser.parse_args()

    query_validator_balances(args.network, args.address)