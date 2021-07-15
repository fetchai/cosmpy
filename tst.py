from src.cosm.auth.auth_rest import AuthRest
from src.cosm.auth.auth_h import AuthWrapper


address="fetch1h6974x4dspft29r9gyegtajyzaht2cdh0rt93w"

auth = AuthWrapper(AuthRest("http://127.0.0.1:1317"))

res = auth.query_account(address=address)
print(res)
