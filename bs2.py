'''移動停損'''

'''績效爛 應該有寫錯 固定績效較好'''


import backtest_function
from talib.abstract import*

I020=backtest_function.GetI020()

#TakeProfit=20
StopLoss=30

TotalProfit=[0]
TotalProfit2=[0]


for date in backtest_function.GetDate(I020):
    Data=[i for i in I020 if i[0]==date]

    TAKBar = backtest_function.ConvertTAKBar(date,Data)

    index=0

    for i in range(1,len(TAKBar['time'])):
        thisTime = TAKBar['time'][i]
        thisClose = TAKBar['close'][i]
        lastClose = TAKBar['close'][i-1]
        
        #price=TAKBar['close'][i] #
        

        if index==0:
            if lastClose - thisClose >30:
                index=-1
                OrderTime = thisTime
                OrderPrice = thisClose
                         

            elif thisClose - lastClose >30:
                index=1
                OrderTime = thisTime
                OrderPrice = thisClose
          

            elif i == len(TAKBar['time'])-1:
              # print(date,'No Trade')
               break

        elif index!=0:
            if index ==1:  
                TmpHigh = OrderPrice
                TrailingStop = TmpHigh-20
                if thisClose > TmpHigh:
                    TmpHigh=thisClose
                    TrailingStop = TmpHigh-20


                    # 贏不到20
                    if thisClose - OrderPrice < 20:

                        if thisClose <= OrderPrice - StopLoss:
                            index=0
                            CoverTime = thisTime			
                            CoverPrice = thisClose
                            Profit = CoverPrice - OrderPrice
                            TotalProfit.append(TotalProfit[-1] + Profit)
                            TotalProfit2.append(Profit)
                            break
                    # 贏20後不輸   
                    elif thisClose - OrderPrice >= 20:
                                       
                        # 不輸贏出場 或 拉回20出場
                        if thisClose <= OrderPrice or thisClose <= TrailingStop:
                            index=0
                            CoverTime = thisTime			
                            CoverPrice = thisClose
                            Profit = CoverPrice - OrderPrice
                            TotalProfit.append(TotalProfit[-1] + Profit)
                            TotalProfit2.append(Profit)
                            break
                            
                      
##                TmpHigh = OrderPrice
##                TrailingStop = TmpHigh-StopLoss
##                
##                if thisClose > TmpHigh:
##                # 重新計算移動停損點
##                    TmpHigh=thisClose
##                    TrailingStop = TmpHigh-StopLoss
##                
##                    if thisClose <= TrailingStop or thisClose <= OrderPrice - StopLoss:
##                        CoverTime = thisTime			
##                        CoverPrice = thisClose
##                        Profit = CoverPrice - OrderPrice
##                        TotalProfit.append(TotalProfit[-1] + Profit)
##                       # print('B','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
##                        break

                
            elif index ==-1:               
                TmpLow = OrderPrice
                TrailingStop = TmpLow+20
                if thisClose < TmpLow:
                    TmpLow=thisClose
                    TrailingStop = TmpLow+20

                    # 贏不到20
                    if OrderPrice-thisClose < 20:
                        if thisClose >= OrderPrice + StopLoss:
                            index=0
                            CoverTime = thisTime			
                            CoverPrice = thisClose
                            Profit = OrderPrice-CoverPrice 
                            TotalProfit.append(TotalProfit[-1] + Profit)
                            TotalProfit2.append(Profit)
                            break
                    # 贏20後不輸   
                    elif OrderPrice-thisClose >= 20:
                        # 不輸贏出場 或 拉回20出場
                        if thisClose >= OrderPrice or thisClose >= TrailingStop:
                            index=0
                            CoverTime = thisTime			
                            CoverPrice = thisClose
                            Profit = OrderPrice-CoverPrice 
                            TotalProfit.append(TotalProfit[-1] + Profit)
                            TotalProfit2.append(Profit)
                            break

                              
##                # 紀錄當前最低價
##                TmpLow = OrderPrice
##                # 初始化移動停損
##                TrailingStop = TmpLow+StopLoss
##
##                if thisClose < TmpLow:
##                # 重新計算移動停損點
##                    TmpLow=thisClose
##                    TrailingStop = TmpLow+StopLoss
##                
##                    if thisClose >= TrailingStop or thisClose >= OrderPrice + StopLoss:
##                        CoverTime = thisTime
##                        CoverPrice = thisClose  	
##                        Profit = OrderPrice - CoverPrice
##                        TotalProfit.append(TotalProfit[-1] + Profit)
##                       # print('S','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
##                        break

# 載入繪圖套件
import matplotlib.pyplot as plt                    
                    
# 定義圖表物件        
ax = plt.subplot(111)

# 繪製圖案
#print(TotalProfit)
ax.plot(range(len(TotalProfit)),TotalProfit, 'k-')

# 定義title
plt.title('Profit Line')

# 顯示繪製圖表
plt.show()
### 儲存圖表
###plt.savefig('Total Profit.png')
##

import pandas as pd
#勝率 (獲利次數 / 交易總筆數)
v=0
for i in TotalProfit2:
    if i>0:
        v+=1                

#獲利因子 = 總收入/(-總虧損) >0  1.5  2
w=[]
l=[]
for i in TotalProfit2:
    if i>=0:
        w.append(i)
    elif i<0:
        l.append(i)

w1=sum(w)
l1=sum(l)                


dic={'交易總筆數':[len(TotalProfit2)],
'總淨利':[sum(TotalProfit2)],
'勝率':['{:.2f}'.format(v/len(TotalProfit2))],
'獲利因子':['{:.2f}'.format(w1/(-l1))]}        

# #橫向
df=pd.DataFrame(dic)  
# print(df)

#縱向
df1=df.T
print(df1)