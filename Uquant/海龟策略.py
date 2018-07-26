#真海龟，在伪海龟的基础上加入仓位控制
#伪海龟（买入的仓位不按照规矩来）
import math
import numpy as np
start = '2018-01-01 '                     # 回测起始时间
end = '2018-4-01'                        # 回测结束时间
universe = ['000001.ZICN']       # 证券池，支持股票、基金、期货、指数四种资产
benchmark = '000001.ZICN'                        # 策略参考标准
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易 
#max_history_window =70
accounts = {
    'xy': AccountConfig(account_type='index', capital_base=1000000)
}

def CheckPosition(position): # 0为未持仓，1为持多，-1为持空 
    try:
        if position['long_amount']==0 and position['short_amount']==0:
            return 0
        elif position['long_amount']!=0 :
            return 1
        elif position['short_amount']!=0:
            return -1
        else:
            return 0
    except:
        return 0
R=0.2 #risk exposure
CN=1  #

def CheckUnit(money,price,atr):
    tmp1=money*R/(atr*CN)
    tmp2=round(tmp1/price)
    if (tmp2!=0):
        return tmp2 
    else:
        return 10000

def Check_LongCost(position):
    tmp=position['long_cost']
    return tmp

def Check_ShortCost(position):
    tmp=position['short_cost']
    return tmp
 
def initialize(context):
    context.position_state=0 #持仓状态，0空仓，1多头，-1空头

def handle_data(context):    
    TR=[]
    ATR20=[]
    ATR10=[]

   
    xy=context.get_account('xy')
        # 记录当前持仓
    
    position =xy.position
    position = dict(position)
   
    if len(position)>0:                          ######### 这部分要注意的！！！！！！！
        position = position[position.keys()[0]]  #python3.5中dict.keys()返回值不是list类型，需要注意
        
    context.position_state =  CheckPosition(position)  # 持仓状态，1则为多头，-1位空头，0为未持仓
    #aclose = get_symbol_history('000001.ZICN',attribute=['closePrice'], freq='1d',time_range=1)
    #aclose=np.array(aclose['closePrice'])
    #print(aclose)

    data=context.history(['000001.ZICN'], ['highPrice','lowPrice','closePrice'] ,30 ,freq='1d', rtype='frame', style='sat')
    aclose=(data['000001.ZICN']['closePrice'])
    bhigh=(data['000001.ZICN']['highPrice'])
    clow=(data['000001.ZICN']['lowPrice'])
    
    Close=np.array(aclose)
    High=np.array(bhigh)
    Low=np.array(clow)
    t1=High[1:]-Low[1:]
    t2=abs(High[1:]-Close[:-1])
    t3=abs(Close[:-1]-Low[1:])
    for i in range(29):
        TR.append(max(t1[i],t2[i],t3[i]))
    for i in range(len(TR)-20):
        tmp=TR[i:i+20]
        ATR20.append(np.mean(tmp))
    for i in range(len(TR)-10):
        tmp=TR[i:i+10]
        ATR10.append(np.mean(tmp))
     
     
    #volatility=ATR20[-1]*CN
    t11= context.current_price('000001.ZICN') #当前价
    t22= (aclose[0])                         #ATR指标开始时的价格
    t33=t11-t22                              #当前价和统计初期价格之差
    
    #value=(xy.portfolio_value)
    ATR=ATR20[-1]
    volatility=ATR*CN
     
    if (context.position_state==0):  #空仓，去开仓
        if (aclose[-1]>bhigh[-2]+0.5*ATR10[-2]):     
            number=CheckUnit(xy.cash,t11,ATR)       # 引用CheckUnit 计算买入量，和R有关       
            xy.order('000001.ZICN', number  , 'open') #多头开仓
        elif(aclose[-1]<clow[-2]-0.5*ATR10[-2]):
            number=CheckUnit(xy.cash,t11,ATR)       
            xy.order('000001.ZICN', -1*number  , 'open')#空头开仓
            

    print(context.position_state)
 
       
             ####################持有多单情况下 
    if (context.position_state==1):
        
        HoldingCost=Check_LongCost(position)
        
        if (t11>=HoldingCost+0.5*ATR):              ####################情况好，加仓unit
            number=CheckUnit(xy.cash,t11,ATR)
            xy.order('000001.ZICN',number,'open')
        elif(ATR10[-1]<ATR):                          # 下降离场(死叉，多头离场)
            xy.close_all_positions('000001.ZICN')
        elif(t22+3*ATR>bhigh[-2]):                #开始统计周期的价格与前一日的最高价之差大于bigfloat*ATR
            if(t11<max(aclose)-2*ATR):             #当前价格自近期最高价下降drawback*ATR,多头平仓
                xy.close_all_positions('000001.ZICN') #多头止盈
        elif(t11<HoldingCost-2*ATR):                   #多头止损，价格下降2ATR强平离场
            xy.close_all_positions('000001.ZICN')
            

            #####持有空单的情况下
    if (context.position_state==-1):  
        
        HoldingCost=Check_ShortCost(position)
        
        if(t11<=HoldingCost-0.5*ATR):  ##价格下降，比持仓成本还低0.5ATR时，加仓unit 
            number=CheckUnit(xy.cash,t11,ATR)
            xy.order('000001.ZICN', number , 'open')    #跌得好，加仓

        elif(ATR<=ATR10[-1]):        #快速上涨，离场(金叉，空头离场)
            xy.close_all_positions('000001.ZICN')
        elif(abs(t22-clow[-2])>3*ATR):         #开始统计周期的价格与前一日最低价之差大于bigfloat*ATR
             if (t11<min(aclose)-2*ATR):
                    xy.close_all_positions('000001.ZICN')  #空头止盈
                   
        elif(t11>HoldingCost+2*ATR):         # 空头止损，价格上涨2ATR离场
            xy.close_all_positions('000001.ZICN')
      
##################
###################################
######################
#伪海龟（买入的仓位不按照规矩来）
import math
import numpy as np
start = '2018-01-01 '                     # 回测起始时间
end = '2018-4-01'                        # 回测结束时间
universe = ['000001.ZICN']       # 证券池，支持股票、基金、期货、指数四种资产
benchmark = '000001.ZICN'                        # 策略参考标准
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易 
#max_history_window =70
accounts = {
    'xy': AccountConfig(account_type='index', capital_base=1000000)
}

def CheckPosition(position): # 0为未持仓，1为持多，-1为持空 
    try:
        if position['long_amount']==0 and position['short_amount']==0:
            return 0
        elif position['long_amount']!=0 :
            return 1
        elif position['short_amount']!=0:
            return -1
        else:
            return 0
    except:
        return 0
value=[]
value.append(100000)
def initialize(context):
    context.position_state=0 #持仓状态，0空仓，1多头，-1空头

R=0.2 #risk exposure
CN=1  #

def handle_data(context):    
    TR=[]
    ATR20=[]
    ATR10=[]

   
    xy=context.get_account('xy')
        # 记录当前持仓
    
    position =xy.position
    position = dict(position)
    
    if len(position)>0:
        position = position[position.keys()[0]]  
         
    context.position_state =  CheckPosition(position)  # 持仓状态，1则为多头，-1位空头，0为未持仓
    #aclose = get_symbol_history('000001.ZICN',attribute=['closePrice'], freq='1d',time_range=1)
    #aclose=np.array(aclose['closePrice'])
    #print(aclose)
    
    

    data=context.history(['000001.ZICN'], ['highPrice','lowPrice','closePrice'] ,30 ,freq='1d', rtype='frame', style='sat')
    aclose=(data['000001.ZICN']['closePrice'])
    bhigh=(data['000001.ZICN']['highPrice'])
    clow=(data['000001.ZICN']['lowPrice'])
    
    Close=np.array(aclose)
    High=np.array(bhigh)
    Low=np.array(clow)
    t1=High[1:]-Low[1:]
    t2=abs(High[1:]-Close[:-1])
    t3=abs(Close[:-1]-Low[1:])
    for i in range(29):
        TR.append(max(t1[i],t2[i],t3[i]))
    for i in range(len(TR)-20):
        tmp=TR[i:i+20]
        ATR20.append(np.mean(tmp))
    for i in range(len(TR)-10):
        tmp=TR[i:i+10]
        ATR10.append(np.mean(tmp))
     
     
    #volatility=ATR20[-1]*CN
    t11= context.current_price('000001.ZICN') #当前价
    t22= (aclose[0])                         #ATR指标开始时的价格
    t33=t11-t22                              #当前价和统计初期价格之差
    
    #value=(xy.portfolio_value)
    ATR=ATR20[-1]
    volatility=ATR*CN
     
    if (context.position_state==0):  #空仓，去开仓
        if (aclose[-1]>bhigh[-2]+0.5*ATR10[-2]):    #多头
            number=math.floor(0.7*xy.cash/t11) # 先用70%资金call       
            xy.order('000001.ZICN', number+1  , 'open') #多头开仓
        elif(aclose[-1]<clow[-2]-0.5*ATR10[-2]):
            number=math.floor(0.7*xy.cash/t11)  #下降厉害的情况下做空用60%
            xy.order('000001.ZICN', -1*number  , 'open')#空头开仓
            

    print(context.position_state)
 
          
             ####################持有多单情况下 
    if (context.position_state==1):
        if (aclose[-1]>=aclose[-2]+ATR):              ####################情况好，加仓
             xy.order('000001.ZICN', round(xy.cash*0.5/t11),'open')
        elif(aclose[-1]<aclose[-2]*0.99):                          #指数下降  ，  多头平仓离开,
            xy.close_all_positions('000001.ZICN')
        elif(t22+2*ATR>bhigh[-2]):                #最开始的进场价格与前一日的最高价之差大于bigfloat*ATR
            if(t11<max(aclose)-2*ATR):             #当前价格自近期最高价下降drawback*ATR,多头平仓
                xy.close_all_positions('000001.ZICN')

            #####持有空单的情况下
    if (context.position_state==-1):              
        if(aclose[-1]<=(aclose[-2]-0.5*ATR)): 
            xy.order('000001.ZICN', -1*round(0.6*xy.cash/t11) , 'open')    #跌得好，加仓

        elif(ATR20[-1]<=ATR10[-1]):        #快速上涨，离场
            xy.close_all_positions('000001.ZICN')

        elif(aclose[-1]>aclose[-2]*1.005):
            xy.close_all_positions('000001.ZICN')
