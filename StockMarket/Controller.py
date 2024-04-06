
from flask import Flask, request
from initilization import Credentials
from Service import ServiceClass

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import json

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
 
    return jsonify(response)


@app.route('/live-data', methods=['GET'])
def getLiveData():
    global liveServerStarted
    accessToken = request.args.get('accessToken')
    searchTicker=request.args.get('searchTicker')
    
    

    if(searchTicker=='NIFTYBANK' or searchTicker=='NIFTY50'):
        service.startliveData(accessToken,searchTicker,'INDEX')
            # liveServerStarted.append(searchTicker)
    else:
        service.startliveData(accessToken,searchTicker,'EQ')
        liveServerStarted.append(searchTicker)

    
    return jsonify(service.getLiveData())

if __name__ == '__main__':
    app.run(debug=True)
