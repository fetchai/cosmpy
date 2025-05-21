# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
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
"""Integration tests for contract functions."""
from pathlib import Path

import pytest
from jsonschema import ValidationError

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.aerial.wallet import LocalWallet


CONTRACT_PATH = Path(__file__).parent / "../../contracts/simple/simple.wasm"
SCHEMA_PATH = Path(__file__).parent / "../../contracts/simple/schema"


class ValidationTestFailure(Exception):
    """Validation test failure exception"""


MAX_FLAKY_RERUNS = 3
RERUNS_DELAY = 10


class TestContract:
    """Test contract"""

    def _get_network_config(self):
        """Get network config."""
        return NetworkConfig.fetchai_stable_testnet()

    def get_wallet(self):
        """Get wallet"""
        wallet = LocalWallet.generate()
        faucet_api = FaucetApi(self._get_network_config())
        faucet_api.get_wealth(wallet.address())
        return wallet

    def get_ledger(self):
        """Get ledger"""
        return LedgerClient(self._get_network_config())

    def get_contract(self):
        """Get contract"""
        return LedgerContract(CONTRACT_PATH, self.get_ledger())

    @pytest.mark.integration
    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS, reruns_delay=RERUNS_DELAY)
    def test_contract(self):
        """Test simple contract deploy execute and query."""
        wallet = self.get_wallet()
        contract = self.get_contract()
        contract_address = contract.deploy({}, wallet)
        assert contract_address
        result = contract.query({"get": {"owner": str(wallet.address())}})

        assert not result["exists"]
        assert not result["value"]

        value = "foobar"
        contract.execute({"set": {"value": value}}, wallet).wait_to_complete()
        result = contract.query({"get": {"owner": str(wallet.address())}})

        assert result["exists"]
        assert result["value"] == value

    @pytest.mark.integration
    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS, reruns_delay=RERUNS_DELAY)
    def test_deployed_contract(self):
        """Test interaction with already deployed contract."""
        wallet = self.get_wallet()
        ledger = self.get_ledger()
        contract = self.get_contract()

        # manual store
        if not contract._code_id:  # pylint: disable=protected-access
            contract.store(wallet)

        # instatiate by code_id
        contract = LedgerContract(
            None, ledger, code_id=contract._code_id  # pylint: disable=protected-access
        )
        contract_address = contract.instantiate(
            {}, wallet, admin_address=wallet.address()
        )
        assert contract_address

        # use by address
        deployed_contract = LedgerContract(None, ledger, contract_address)

        result = deployed_contract.query({"get": {"owner": str(wallet.address())}})

        assert not result["exists"]
        assert not result["value"]

        value = "foobar"
        deployed_contract.execute({"set": {"value": value}}, wallet).wait_to_complete()
        result = deployed_contract.query({"get": {"owner": str(wallet.address())}})

        assert result["exists"]
        assert result["value"] == value

        # Upgrade contract
        original_contract_address = contract.address
        original_code_id = contract.code_id

        tx_res = deployed_contract.upgrade({}, wallet, CONTRACT_PATH)
        assert tx_res.response
        assert deployed_contract.address == original_contract_address
        assert deployed_contract.code_id != original_code_id

        # Change admin from wallet to wallet2
        wallet2 = self.get_wallet()
        tx_res = deployed_contract.update_admin(wallet, wallet2.address())
        assert tx_res.response

        # New admin calls clear admin
        tx_res = deployed_contract.update_admin(wallet2, None)
        assert tx_res.response

    @pytest.mark.integration
    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS, reruns_delay=RERUNS_DELAY)
    def test_contract_schema_validation(self):
        """Test simple contract schema validation."""
        wallet = self.get_wallet()
        contract = LedgerContract(
            CONTRACT_PATH, self.get_ledger(), schema_path=SCHEMA_PATH
        )
        contract._address = "asi1r3d4azhlak4w00c5n02t9l35a3n6462vc388mu"  # pylint: disable=protected-access

        try:
            bad_query = {"get_count": 0}
            contract.query(bad_query)
        except ValidationError:
            pass
        except Exception as exc:
            raise ValidationTestFailure("Query should have failed validation") from exc

        try:
            bad_msg = {"increment": 1}
            contract.execute(bad_msg, wallet).wait_to_complete()
        except ValidationError:
            pass
        except Exception as exc:
            raise ValidationTestFailure("Msg should have failed validation") from exc

        try:
            bad_msg = {"bad": 1}
            contract.migrate(bad_msg, wallet, 1).wait_to_complete()
        except ValidationError:
            pass
        except Exception as exc:
            raise ValidationTestFailure("Msg should have failed validation") from exc


class TestContractRestAPI(TestContract):
    """Test dorado rest api"""

    def _get_network_config(self):
        return NetworkConfig(
            chain_id="eridanus-1",
            url="rest+https://rest-eridanus-1.fetch.ai:443",
            fee_minimum_gas_price=5000000000,
            fee_denomination="atestasi",
            staking_denomination="atestasi",
            faucet_url="https://faucet-eridanus-1.fetch.ai",
        )


if __name__ == "__main__":
    pytest.main([__file__])
