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

"""REST example of query balance."""

from cosmpy.clients.ledger import CosmosLedger

REST_URL = "http://127.0.0.1:1317"
ADDRESS = "fetch128r83uvcxns82535d3da5wmfvhc2e5mut922dw"
DENOM = "atestfet"
CHAIN_ID = "testing"


# Create ledger
ledger = CosmosLedger(chain_id=CHAIN_ID, rest_node_address=REST_URL)
print(f"Balance of {ADDRESS} is {ledger.get_balance(ADDRESS,DENOM)} {DENOM}")
