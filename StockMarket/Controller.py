
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

@app.route('/historicalData', methods=['GET'])
def getHistoryData():
    global liveServerStarted
    time_frame=''
    accessToken = request.args.get('accessToken')
    searchTicker=request.args.get('searchTicker')
    time_frame=request.args.get('time_frame')
    range_from=request.args.get('startDate')
    range_to=request.args.get('endDate')
    
    print(searchTicker,time_frame,range_from,range_to)
    time_frame_dict = {"5 seconds": "5S","10 seconds": "10S","15 seconds": "15S","30 seconds": "30S","45 seconds": "45S","1 minute": "1","2 minute": "2","3 minute": "3","5 minute": "5","10 minute": "10","15 minute": "15", "20 minute": "20","30 minute": "30","60 minute": "60","120 minute": "120","240 minute": "240","1 Day":"D"}
    if(searchTicker=="NIFTY50" or searchTicker=="NIFTYBANK"):
        return service.get_historicalData(accessToken,f'NSE:{searchTicker}-INDEX',time_frame_dict[time_frame],"1",range_from,range_to)
    else:
        return service.get_historicalData(accessToken,f'NSE:{searchTicker}-EQ',time_frame_dict[time_frame],"1",range_from,range_to)
    


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
print("Server Started on port http://127.0.0.1:5000") 
if __name__ == '__main__':
    
    app.run(debug=True)
