# -*- coding: utf-8 -*-
"""
a sample to show how to utilize the realtime watching function
"""
import sys

sys.path.insert(0, "../")
import xalpha as xa
import pandas as pd

# first introduce some aim you want to watch
# you must use rfundinfo instead of standard fundinfo class to get the realtime netvalue

fundNum = ["001838", "501057", "003095"]



n = 0


down_fund = [0, 0, 0, 0, 0, 0]
downPercent = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1]

path = "fund2021.csv"

read = xa.record(path) 
read.status
sysopen = xa.mul( status = read.status ) 

def get_mul_targetPrice(fundNum):
    df = sysopen.combsummary()

    df_fund_cost = df.loc[df['基金代码']==fundNum, ['单位成本']]
    # df_GTRY_JunGong_cost = df.loc[df['基金代码']=='001838', ['单位成本']]
    # df_YFD_LanChou_cost = df.loc[df['基金代码']=='005827', ['单位成本']]
    # df_ZhO_XinLanChou_cost = df.loc[df['基金代码']=='166002', ['单位成本']]

    #df501057_cost.to_csv("d:\\tmp\\501057_cost.csv", encoding='utf_8_sig')

    #down = cal_downvalue(0.05)
    #df501057_cost['跌5%'] = range(down5,len(df501057_cost)+1)

    oriNetValue_fund = df_fund_cost.iloc[-1, -1]

    i = 0
    for i in range(0,6):
        down_fund[i] = oriNetValue_fund - oriNetValue_fund * downPercent[i]

        print("downPercent" +str(i)+ " = " +str(downPercent[i]))
        print("down_fund"+str(i)+" = " + str(down_fund[i]))

def autoInvest(fundMessage, fundNum):
    DQbuDE_fund = xa.policy.scheduled_tune(
                fundMessage, 
                100, 
                times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
                piece=[(down_fund[0], 5),(down_fund[1], 6),(down_fund[2], 7)]) 

    print("========================================")
    print("down_GTRY_JunGong[0] = " + str(down_fund[0]))
    print("down_GTRY_JunGong[1] = " + str(down_fund[1]))
    print("down_GTRY_JunGong[2] = " + str(down_fund[2]))

for n in range(0, 3):
    fundMessage = xa.rfundinfo(fundNum[n])
    print("--------------- fundNum ----------------  = " + str(fundNum[n]))

    get_mul_targetPrice(fundNum[n])
    autoInvest(fundMessage, down_fund[0:6])