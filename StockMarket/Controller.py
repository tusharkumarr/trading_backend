
from flask import Flask, request
from initilization import Credentials
from Service import ServiceClass

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import json
import logging

app = Flask(__name__)
CORS(app)
service=ServiceClass()


liveServerStarted=[]

@app.route('/generate-link', methods=['GET'])
async def generateLink():
    
    user = request.args.get('user')  

    
    link = await service.generateLink(user)
    
    # print(link)

    # Return the generated link as JSON response
    return jsonify({'link': link})

@app.route('/access-code', methods=['GET'])
async def access_code():
    authCode = request.args.get('authCode')
    response = await service.getAccessCode(authCode)
    

 
    return jsonify(response)


@app.route('/get-profile', methods=['GET'])
async def getprofile():
    accessToken = request.args.get('accessToken')

    
    
    response = await service.getProfile(accessToken)
    symbols1=["NIFTY50","NIFTYBANK",
        "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "BHARTIARTL", "ITC", "SBIN", "LICI",
        "LT", "BAJFINANCE", "HCLTECH", "KOTAKBANK", "AXISBANK", "ASIANPAINT", "TITAN", "ADANIENT", "MARUTI",
        "ULTRACEMCO", "SUNPHARMA", "NTPC", "BAJAJFINSV", "DMART", "TATAMOTORS", "ONGC", "NESTLEIND", "ADANIGREEN",
        "WIPRO", "COALINDIA", "ADANIPORTS", "POWERGRID", "JSWSTEEL", "M&M", "ADANIPOWER", "BAJAJ-AUTO", "HAL",
        "LTIM", "IOC", "DLF", "TATASTEEL", "VBL", "JIOFIN", "SBILIFE", "SIEMENS", "GRASIM", "HDFCLIFE", "HINDALCO",
        "PIDILITIND", "BEL", "HINDZINC", "IRFC", "BRITANNIA", "PFC", "INDUSINDBK", "TECHM", "BANKBARODA", "ADANIENSOL",
        "GODREJCP", "INDIGO", "EICHERMOT", "RECLTD", "ATGL", "TRENT", "ZOMATO", "GAIL", "TATAPOWER", "CHOLAFIN",
        "PNB", "DIVISLAB", "AMBUJACEM", "SHREECEM", "TATACONSUM", "CIPLA", "ABB", "DABUR", "LODHA", "BPCL", "DRREDDY",
        "TVSMOTOR", "VEDL", "UNIONBANK", "HAVELLS", "BAJAJHLDNG", "POLYCAB", "APOLLOHOSP", "IOB", "MCDOWELL-N", "MANKIND",
        "CANBK", "TORNTPHARM", "IDEA", "SHRIRAMFIN", "ICICIPRULI", "JINDALSTEL", "SRF", "IDBI", "SBICARD", "IRCTC"

    ]
    new_Symbol=[]

    for i in symbols1:
        if(i=="NIFTY50" or i=="NIFTYBANK"):

            new_Symbol.append(f'NSE:{i}-INDEX')
        else:
            new_Symbol.append(f'NSE:{i}-EQ')
    service.startliveData(accessToken,new_Symbol)

    return jsonify(response)


@app.route('/live-data', methods=['GET'])
def getLiveData():
    global liveServerStarted
    accessToken = request.args.get('accessToken')
    searchTicker=request.args.get('searchTicker')
    
    return jsonify(service.getLiveData()[searchTicker])

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
print("Server Started on port http://127.0.0.1:5000") 
if __name__ == '__main__':
    
    app.run(debug=True)
