from cosm.bank.rest_client import BankRestClient, QueryBalanceRequest

REST_URL = "http://127.0.0.1:1317"
ADDRESS = "fetch1mrf5yyjnnlpy0egvpk2pvjdk9667j2gtu8kpfy"
DENOM = "stake"

bank = BankRestClient(REST_URL)
res = bank.Balance(QueryBalanceRequest(address=ADDRESS, denom=DENOM))
print(f"Balance of {ADDRESS} is {res.balance.amount} {res.balance.denom}")
