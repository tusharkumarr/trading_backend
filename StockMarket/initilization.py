from fyers_api import accessToken
import fyers_api
class Credentials:
   
    def __init__(self):
        self.name="ravi"
        self.client_id = "O6E68XFF4T-100"
        self.secret_key = "XD704EK79E"
        self.redirect_uri = "https://www.google.com/"
        self.response_type = "code"
        self.state = "sample_state"
    def greet(self):
        return f"hello, {self.name}"
    def getResponseLink(self):

        session=accessToken.SessionModel(
        client_id=self.client_id,
        secret_key=self.secret_key,
        redirect_uri=self.redirect_uri, 
        response_type=self.response_type
        )

        response = session.generate_authcode()

        return  f'<a href="{response}">{response}</a>'