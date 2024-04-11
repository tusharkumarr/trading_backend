from datetime import datetime
class ExecuteTrade:
    all_trade=[{}]
    curr_trade={"ticker":'',"buy_time":'','sell_time':'','quantity':'','buy_price':'','sell_price':'','p&l':''}
    def __init__(self) -> None:
        self.all_trade=[{"ticker":'',"buy_time":'','sell_time':'','quantity':'','buy_price':'','sell_price':'','p&l':''}]
        
        pass
    def getAllTrade(self):
        return self.all_trade
    def executeTrade(self,ticker,quantity,buy_price,sell_price):
        try:
            last_trade=self.all_trade[len(self.all_trade)-1]
            if(last_trade['buy_price']!='' and last_trade['sell_price']!=''):
                self.all_trade.append({"ticker":'',"buy_time":'','sell_time':'','quantity':'','buy_price':'','sell_price':'','p&l':''})
                last_trade=self.all_trade[len(self.all_trade)-1]

            if(last_trade['buy_price']==''):# for buying the strike
                last_trade["ticker"]=ticker
                last_trade["buy_time"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                last_trade['quantity']=quantity
                last_trade['buy_price']=buy_price
            

            else:
                last_trade['sell_price']=sell_price
                last_trade["sell_time"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(last_trade)
            # last_trade["p&l"]=int(last_trade['sell_price'])-int(last_trade['buy_price'])
            self.all_trade[len(self.all_trade)-1]=last_trade
        except Exception as e:
            print(e)
        

        
