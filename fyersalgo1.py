from fyers_api import accessToken
import fyers_api
client_id = "O6E68XFF4T-100"
secret_key = "XD704EK79E"
redirect_uri = "https://www.google.com/"
response_type = "code"
state = "sample_state"

session=accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri, 
    response_type=response_type
)

response = session.generate_authcode()



print(response)
redirect_uri='https://www.google.com/?s=ok&code=200&auth_code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTEyNjU2MjIsImV4cCI6MTcxMTI5NTYyMiwibmJmIjoxNzExMjY1MDIyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImF1dGhfY29kZSIsImRpc3BsYXlfbmFtZSI6IllBMDQwMTQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOm51bGwsIm5vbmNlIjoiIiwiYXBwX2lkIjoiTzZFNjhYRkY0VCIsInV1aWQiOiJiN2ExYjAwYjNhMDg0MzA2YTllNTFmNDA1NmI3YzdjZCIsImlwQWRkciI6IjEwMy4yMTEuMTcuMjU0Iiwic2NvcGUiOiIifQ.9Is8q1uXEAnYG7Um0tOPZcFYVP23lWjOQuB_J4WmmtA&state=None'

session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type="authorization_code"
)
session.set_token(response)
response = session.generate_token()
print(response)