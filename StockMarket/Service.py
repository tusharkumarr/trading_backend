from fyers_api import accessToken

from fyers_apiv3 import fyersModel
from datetime import datetime
from fyers_apiv3.FyersWebsocket import data_ws
import asyncio
import numpy as np
import datetime

class ServiceClass:
    response_data = {"":[]}
    interadayHistoryDataMinute={"":[]}
    liveRSI={"":[]}
  
    
    def __init__(self):
        self.client_id = "KLOTU3GDY4-100"#tushar
        # self.client_id ="U2K5ZXGCCS-100" #SAMAR
        self.secret_key = "85XIIXI8CD" #TUSHAR
        # self.secret_key = "1JUDGO30RE" #samar
        self.redirect_uri = "https://www.google.com/"
        self.response_type = "code"
        self.state = "sample_state"
        self.response_data = {}
        self.interadayHistoryDataMinute={}
        self.liveRSI={}
       
        
        

    
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
    def getHistoryData_in_minute(self):
        return self.interadayHistoryDataMinute
  
    def startliveData(self,access_token,symbols):
        try:
            data_type = "SymbolUpdate"
        
            def onmessage(message):
                if "symbol" in message:
                    if(message["symbol"].endswith("-EQ")):
                        ticker=message["symbol"].split(":")[1].split("-EQ")[0]
                    
                    else:
                        ticker=message["symbol"].split(":")[1].split("-INDEX")[0]

                
                    if self.response_data is not None and ticker in self.response_data:
                        if('code' not in message): 
                            self.response_data[ticker].append(message)
                            datetime_obj = datetime.datetime.fromtimestamp(message['exch_feed_time'])
                        
                            datetime_obj_LastRec=datetime.datetime.fromtimestamp(self.interadayHistoryDataMinute[ticker][len(self.interadayHistoryDataMinute[ticker])-1]['exch_feed_time'])
                        
                        
                            min=datetime_obj.minute
                            if(datetime_obj_LastRec.minute!=min):
                            
                                self.interadayHistoryDataMinute[ticker].append(message)

                    else:
                
                        if('code' not in message):
                            self.response_data[ticker] = [message]
                            self.interadayHistoryDataMinute[ticker]=[message]
                        
                            
                        
                # self.response_data[ticker]=self.response_data[ticker]

            # fyers.unsubscribe(symbols=[f'NSE:{searchTicker}-INDEX'], data_type="SymbolUpdate")



            def onerror(message):

                print("Error:", message)


            def onclose(message):
                print("Connection closed:", message)
                # fyers.subscribe(symbols=symbols, data_type=data_type)
         
  


            def onopen():

            
          
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
        except Exception as e:
            print("error :", e)
        
    
    def get_historicalData(self,access_token,symbol,resolution,date_format,range_from,range_to):
        
        fyers = fyersModel.FyersModel(client_id=self.client_id, is_async=False, token=access_token, log_path="")

        data = {
            "symbol":symbol,
            "resolution":resolution,
            "date_format":date_format,
            "range_from":range_from,
            "range_to":range_to,
            "cont_flag":"1"
        }

        response = fyers.history(data=data)
        return response
    
    def get_close_price(self,response):
        close_price_temp = []
        
        for i in response.get('candles', []):
            
            close_price_temp.append(i[4])
        
    
        return close_price_temp
    
    def calculate_rsi(self,closing_prices, window=14):
        rsi=[]
       
        closing_prices=np.array(closing_prices)
        
        deltas = np.diff(closing_prices)
        seed = deltas[:window+1]
        up = seed[seed >= 0].sum() / window
        down = -seed[seed < 0].sum() / window
        if(up==0 or down==0):
            return []
            
        rs = up / down
        rsi = np.zeros_like(closing_prices)
        rsi[:window] = 100. - 100. / (1. + rs)

        for i in range(window, len(closing_prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
        
            up = (up * (window - 1) + upval) / window
            down = (down * (window - 1) + downval) / window

            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)

        return rsi.tolist()


        


