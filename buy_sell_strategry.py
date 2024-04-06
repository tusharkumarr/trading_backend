import random

# Generate a random integer between 1 and 100
rsi=[]
for i in range(1,10000):
    rsi.append(random.randint(20, 95))


order=[]
temp={}
buy=0
sell=0
for i in range(1000):
    if(rsi[i]>=30 and rsi[i]<=32 and buy==0 and sell==0):
        temp["buy-price"]=rsi[i]
        temp["buy_ind"]=i
        buy=1

    if(rsi[i]>=75 and rsi[i]<=85 and sell==0 and buy==1):
        temp["sell-price"]=rsi[i]
        temp["sell_ind"]=i
        order.append(temp)
        temp={}
        buy=0

print(order)
