from cosm.bank.bank_h import Bank

rest_address = "http://127.0.0.1:1317"
address = "fetch1h6974x4dspft29r9gyegtajyzaht2cdh0rt93w"
denom = "stake"

bank = Bank(rest_address)
response = bank.query_params()

print(response)
