from cosm.bank.rest_client import BankRestClient, QueryBalanceRequest

auth = BankRestClient("http://127.0.0.1:1317")
address = "fetch1mrf5yyjnnlpy0egvpk2pvjdk9667j2gtu8kpfy"
denom = "stake"

res = auth.Balance(QueryBalanceRequest(address=address, denom=denom))
print(f"Balance of {address} is {res.balance.amount} {res.balance.denom}")
