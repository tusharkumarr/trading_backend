
from flask import Flask, request
from initilization import Credentials
from Service import ServiceClass

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from Trade import ExecuteTrade
import traceback

app = Flask(__name__)
CORS(app, origins="https://8gtlqbzg-3000.inc1.devtunnels.ms")
# CORS(app)
service=ServiceClass()
executeTradeService=ExecuteTrade()


liveServerStarted=[]

@app.route('/generate-link', methods=['GET'])
async def generateLink():
    try:

        user = request.args.get('user')  

    
        link = await service.generateLink(user)
    
    # print(link)

    # Return the generated link as JSON response
        return jsonify({'link': link})
    except Exception as e:
        print("Error: ",str(e))
        return jsonify({"error":str(e)})

@app.route('/access-code', methods=['GET'])
async def access_code():
    authCode = request.args.get('authCode')
    response = await service.getAccessCode(authCode)
    

 
    return jsonify(response)


@app.route('/get-profile', methods=['GET'])
async def getprofile():
    try:
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
        selected_columns = ['Symbol']
        df = pd.read_excel('MCAP31122023_0.xlsx', usecols=selected_columns)

        df = df.dropna()
        company_List=[]
        for index, row in df.iterrows():
            company_List.append(row['Symbol'])

        company_List1=company_List[:702]#2190
        symbols1=company_List1
        new_Symbol=[]
        index=["NIFTY50","NIFTYBANK","FINNIFTY"]
        for i in index:
            symbols1.append(i)

        for i in symbols1:
            if(i=="NIFTY50" or i=="NIFTYBANK" or i=="FINNIFTY" ):

                new_Symbol.append(f'NSE:{i}-INDEX')
            else:
                new_Symbol.append(f'NSE:{i}-EQ')
        service.startliveData(accessToken,new_Symbol)

        return jsonify(response)
    except Exception as e:
        print("Error: ",str(e))
        return jsonify({"error":str(e)})


@app.route('/live-data', methods=['GET'])
def getLiveData():
    try:
        global liveServerStarted
        accessToken = request.args.get('accessToken')
        searchTicker=request.args.get('searchTicker')
        if(searchTicker=='M'):
            searchTicker="M&M"
    
        response=service.getLiveData()
        if(searchTicker in response):
            return jsonify(response[searchTicker])
        else:
            return jsonify({"message":"not found"})
    except Exception as e:
        print("Error: ",str(e))
        return jsonify({"error":str(e)})

@app.route('/historicalData', methods=['GET'])
def getHistoryData():
    try:
        global liveServerStarted
        time_frame=''
        accessToken = request.args.get('accessToken')
        searchTicker=request.args.get('searchTicker')
        time_frame=request.args.get('time_frame')
        range_from=request.args.get('startDate')
        range_to=request.args.get('endDate')
    
   
        time_frame_dict = {"5 seconds": "5S","10 seconds": "10S","15 seconds": "15S","30 seconds": "30S","45 seconds": "45S","1 minute": "1","2 minute": "2","3 minute": "3","5 minute": "5","10 minute": "10","15 minute": "15", "20 minute": "20","30 minute": "30","60 minute": "60","120 minute": "120","240 minute": "240","1 Day":"D"}
        if(searchTicker=="NIFTY50" or searchTicker=="NIFTYBANK"):
            return service.get_historicalData(accessToken,f'NSE:{searchTicker}-INDEX',time_frame_dict[time_frame],"1",range_from,range_to)
        else:
            return service.get_historicalData(accessToken,f'NSE:{searchTicker}-EQ',time_frame_dict[time_frame],"1",range_from,range_to)
    except Exception as e:
        print("Error: ",str(e))
        return jsonify({"error":str(e)})
    
@app.route('/filterStocks', methods=['GET'])
def filterStocks():
    try:
        print("started")
        global liveServerStarted
        time_frame=''
        accessToken = request.args.get('accessToken')
        time_frame=request.args.get('time_frame')

        time_frame_dict = {"5 seconds": "5S","10 seconds": "10S","15 seconds": "15S","30 seconds": "30S","45 seconds": "45S","1 minute": "1","2 minute": "2","3 minute": "3","5 minute": "5","10 minute": "10","15 minute": "15", "20 minute": "20","30 minute": "30","60 minute": "60","120 minute": "120","240 minute": "240","1 Day":"D"}
        time_frame_dict1 = {"5 seconds": 5,"10 seconds": 10,"15 seconds": 15,"30 seconds": 30,"45 seconds": 45,"1 minute": 60, "2 minute": 120, "3 minute": 180,"5 minute": 300, "10 minute": 600, "15 minute": 900,"20 minute": 1200,"30 minute": 1800,"60 minute": 3600,"120 minute": 7200,"240 minute": 14400,"1 Day": 86400 }
        selected_columns = ['Symbol']
        df = pd.read_excel('MCAP31122023_0.xlsx', usecols=selected_columns)

        df = df.dropna()
        company_List=[]
        for index, row in df.iterrows():
            company_List.append(row['Symbol'])

        rsi=[]
        company_List1=company_List[:702]#2190
        company_position=[]
        company_Dict_with_55to57_rsi={}
        company_Dict_with_38to40_rsi={}
        today = datetime.now().date()
        start_date = today - timedelta(days=2)

# Define the end date by adding 50 days to the start date
        end_date = today - timedelta(seconds=1)
        start_Date = start_date.strftime("%Y-%m-%d")
        end_Date = end_date.strftime("%Y-%m-%d")
 
        for i in company_List1:
  
            response=service.get_historicalData(accessToken,f"NSE:{i}-EQ",time_frame_dict[time_frame],"1",start_Date,end_Date)
        
            close_price=service.get_close_price(response)
        
            if(len(service.calculate_rsi(close_price))==0):
                continue
            temp=(service.calculate_rsi(close_price))
            # temp=temp.tolist()
            if(len(temp)>0):

                rsi.append(temp[len(temp)-1]),
            if len(temp) > 0 and temp[-1] >= 55 and temp[-1] <= 57:
                if(temp[len(temp)-1]>=55 and temp[len(temp)-1]<=57 ):

                    company_Dict_with_55to57_rsi[i]=temp[len(temp)-45:len(temp)-1]
                elif(temp[len(temp)-1]>=38 and temp[len(temp)-1]<=42):
                    company_Dict_with_38to40_rsi[i]=temp[len(temp)-45:len(temp)-1]
                company_position.append(i)
        print("closed")

 
        return jsonify({"company_Dict_with_38to40_rsi":company_Dict_with_38to40_rsi,"company_Dict_with_55to57_rsi":company_Dict_with_55to57_rsi})
    except Exception as e:
        print("Error: ",str(e))
        return jsonify({"error":str(e)})

@app.route('/interadayHistoryDataMinute', methods=['GET'])
def get_InteradayHistoryDataMinute():
    try:
        global liveServerStarted
        accessToken = request.args.get('accessToken')
        searchTicker=request.args.get('searchTicker')
        # print(searchTicker)
        if(searchTicker=='M'):
            searchTicker="M&M"
    
        response=service.getHistoryData_in_minute()

        close_price=[]
        for i in response[searchTicker]:
            close_price.append(i['ltp'])
        current_ltp=service.getLiveData()[searchTicker][-1]['ltp']
        
        close_price.append(current_ltp)
        # print(close_price)
        rsi_List=(service.calculate_rsi(close_price))

       # Corrected code snippet
        all_trades = executeTradeService.getAllTrade()

        if all_trades and all_trades[-1]['buy_price'] != '':
            if rsi_List:
                if rsi_List[-1] <= 33 and rsi_List[-1] >= 28:
                    executeTradeService.executeTrade(searchTicker, 50, current_ltp, '')
        else:
            if rsi_List:
                if rsi_List[-1] >= 75 and rsi_List[-1] <= 85:
                    executeTradeService.executeTrade(searchTicker, 50, '', current_ltp)

        return jsonify(rsi_List)
    except Exception as e:
    # Code to handle the specific exception (ZeroDivisionError in this case)
        print("Error(location: get_InteradayHistoryDataMinute): ",str(e))
        traceback.print_exc()
        return jsonify({"error":str(e)})

    
    
    # else:
        # return jsonify({"message":"not found"})
@app.route('/getAllTrade', methods=['GET'])
def getAllTrade():
    return executeTradeService.getAllTrade()

@app.route('/getAllRSI', methods=['GET'])
def getAllRSI():

    selected_columns = ['Symbol']
    df = pd.read_excel('MCAP31122023_0.xlsx', usecols=selected_columns)

    df = df.dropna()
    company_List=[]
    for index, row in df.iterrows():
        company_List.append(row['Symbol'])

    rsi={}
    company_List1=company_List[:702]#2190
    response=service.getHistoryData_in_minute()

    for i in company_List1:
        close_price=[]
        if(i in response):
            for j in response[i]:
                close_price.append(j['ltp'])
            # print(service.getLiveData()[str(i)])
       
       
            current_ltp=service.getLiveData()[str(i)][-1]['ltp']
        
            close_price.append(current_ltp)
            rsi_List=(service.calculate_rsi(close_price))
            rsi[i]=rsi_List
    return jsonify({'rsi':rsi})

@app.route('/fillterLiveStocks', methods=['GET'])
def filterLiveStocks():
    response=service.getHistoryData_in_minute()
    close_price=[]
    selected_columns = ['Symbol']
    df = pd.read_excel('MCAP31122023_0.xlsx', usecols=selected_columns)

    df = df.dropna()
    company_List=[]
    for index, row in df.iterrows():
        company_List.append(row['Symbol'])

    rsi={}
    company_List1=company_List[:702]#2190
    
    response=service.getHistoryData_in_minute()

    output={}
    for j in company_List1:
        if j not in response:
            continue
        for i in response[j]:
            close_price.append(i['ltp'])
        current_ltp=service.getLiveData()[j][-1]['ltp']
        
        close_price.append(current_ltp)
        rsi_List=(service.calculate_rsi(close_price))
      
        if(len(rsi_List)>0):
            output[j]=rsi_List[len(rsi_List)-1]




    return jsonify({"output":output})

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
print("Server Started on port http://127.0.0.1:5000") 
if __name__ == '__main__':
    
    app.run(debug=True)
