from fyers_api import accessToken

from fyers_apiv3 import fyersModel
from datetime import datetime
from fyers_apiv3.FyersWebsocket import data_ws
import asyncio

class ServiceClass:
    response_data = {"":[]}
    
    
    def __init__(self):
        self.client_id = "120MCV67H0-100"
        self.secret_key = "YIWKKI1CRJ"
        self.redirect_uri = "https://www.google.com/"
        self.response_type = "code"
        self.state = "sample_state"
        self.response_data = {}
        

    
    async def  generateLink(self,user):
        session=accessToken.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri, 
            response_type=self.response_type
        )

        return session.generate_authcode()
    async def getAccessCode(self,auth_code):
        session = accessToken.SessionModel(
        client_id=self.client_id,
        secret_key=self.secret_key, 
        redirect_uri=self.redirect_uri, 
        response_type=self.response_type, 
        grant_type="authorization_code"
        )
        session.set_token(auth_code)
        response = session.generate_token()
        
        return response
    async def getProfile(self,access_token):
        fyers = fyersModel.FyersModel(client_id=self.client_id, is_async=False, token=access_token, log_path="")
        response = fyers.get_profile()
        return response
    def getLiveData(self):
        return self.response_data
  
    def startliveData(self,access_token,searchTicker,type):
        
        def onmessage(message):
            print(self.response_data)
            if self.response_data is not None and searchTicker in self.response_data:
                if('code' not in message):
                    self.response_data[searchTicker].append(message)
            else:
                if('code' not in message):

                    self.response_data[searchTicker] = [message]
                # self.response_data[searchTicker]=self.response_data[searchTicker]

            # fyers.unsubscribe(symbols=[f'NSE:{searchTicker}-INDEX'], data_type="SymbolUpdate")



        def onerror(message):

            print("Error:", message)


        def onclose(message):
         print("Connection closed:", message)
  


        def onopen():

            data_type = "SymbolUpdate"
            
                
            symbols = [f'NSE:{searchTicker}-{type}']
          
            # print(symbols)
            
            fyers.subscribe(symbols=symbols, data_type=data_type)
            fyers.keep_running()


        fyers = data_ws.FyersDataSocket(
            access_token=access_token,       # Access token in the format "appid:accesstoken"
            log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
            litemode=False,                  # Lite mode disabled. Set to True if you want a lite response.
            write_to_file=False,              # Save response in a log file instead of printing it.
            reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
            on_connect=onopen,               # Callback function to subscribe to data upon connection.
            on_close=onclose,                # Callback function to handle WebSocket connection close events.
            on_error=onerror,                # Callback function to handle WebSocket errors.
            on_message=onmessage             # Callback function to handle incoming messages from the WebSocket.
        )

        fyers.connect()
       
        


