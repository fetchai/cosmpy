from cosm.query.rest_client import RestClient


class Bank:
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def get_balance(self, account_address: str, denom: str):
        return self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{account_address}/{denom}")

    def get_all_balances(self, account_address: str):
        return self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{account_address}")

    def get_total_supply(self):
        return self.rest_api.query(f"/cosmos/bank/v1beta1/supply")

    def get_supply_of(self, denom: str):
        return self.rest_api.query(f"/cosmos/bank/v1beta1/supply/{denom}")

    def get_denoms_metadata(self):
        return self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata")

    def get_metadata_of_denom(self, denom: str):
        return self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata/{denom}")
