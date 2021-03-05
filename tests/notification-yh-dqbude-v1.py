# -*- coding: utf-8 -*-

import sys
from loguru import logger

sys.path.insert(0, "../")
import xalpha as xa
import pandas as pd

logger.add('notifyFund.txt', format="{time} {level} {message}")
logger.info("====== Notify Start =======")


fundNum = ["001838", "501057", "003095", "005847", "163406", "166002", "161005", "005827", "570008"]
fundName = ["《题材 - 军工》", "《题材 - 新能源车》", "《题材 - 医疗》", "《题材 - 港股》",
    "《主动混合 - 兴全和润》", "《主动混合 - 中欧新蓝筹》", "《主动混合 - 富国天惠》", "《主动混合 - 易方达蓝筹》", "《主动混合 - 诺德周期策略》"]

n = 0

downPercent = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
down_fund = [0] * len(downPercent)
DQbuDE_policy_lst = [''] * len(fundNum)
# DQbuDE_policy_lst = ['', '', '', '', '', '', '', '', '']

def get_mul_targetPrice(fundNum):
    path = "fund2021.csv"
    read = xa.record(path) 
    read.status
    sysopen = xa.mul( status = read.status ) 
    df = sysopen.combsummary()
    df_fund_cost = df.loc[df['基金代码']==fundNum, ['单位成本']]
    i = 0

    oriNetValue_fund = df_fund_cost.iloc[-1, -1]

    for i in range(0,len(downPercent)):
        down_fund[i] = round((oriNetValue_fund - oriNetValue_fund * downPercent[i]), 4)

        print("downPercent" +str(i)+ " = " +str(downPercent[i]))
        print("down_fund"+str(i)+" = " + str(down_fund[i]))

def autoInvest(fundMessage, fundNum, n):

    DQbuDE_policy_lst[ n ] = xa.policy.scheduled_tune(
        fundMessage, 
        100,
        times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
        piece=[(down_fund[5], 10),(down_fund[4], 9),(down_fund[3], 8),(down_fund[2], 7),(down_fund[1], 6),(down_fund[0], 5)]) 

    print("========================================")
    print("DQbuDE_policy_lst" + str(n) + "==" + str(DQbuDE_policy_lst[n]))
    print("========================================")
    print("down_Fund[0] = " + str(down_fund[0]))
    print("down_Fund[1] = " + str(down_fund[1]))
    print("down_Fund[2] = " + str(down_fund[2]))
    print("down_Fund[3] = " + str(down_fund[3]))
    print("down_Fund[4] = " + str(down_fund[4]))
    print("down_Fund[5] = " + str(down_fund[5]))

for n in range(0, len(fundNum)):
    fundMessage = xa.rfundinfo(fundNum[n])
    print("--------------- fundNum ----------------  = " + str(fundNum[n]))

    get_mul_targetPrice(fundNum[n])
    autoInvest(fundMessage, down_fund[0:6], n)

k=0
for k in range(0, 9):
    print("DQbuDE_policy_lst" + str(k) +":======" + str(DQbuDE_policy_lst[k]))

check = xa.review([DQbuDE_policy_lst[0], DQbuDE_policy_lst[1], DQbuDE_policy_lst[2], DQbuDE_policy_lst[3], 
    DQbuDE_policy_lst[4], DQbuDE_policy_lst[5], DQbuDE_policy_lst[6], DQbuDE_policy_lst[7], DQbuDE_policy_lst[8]], 
    [fundName[0], fundName[1], fundName[2], fundName[3], fundName[4], fundName[5], fundName[6], fundName[7], fundName[8]])

conf = {
    "sender": "zyhmike@126.com",
    "sender_name": "YH",
    "receiver": ["yuhang@sgstudios.cn", "zyhmike@126.com"],
    "password": "PFDBTYIXTOMLNJXB",
    "server": "smtp.126.com",
    "port": 465,
    "receiver_name": ["me", "zyhmike"],
}

# finally send the notification
check.notification(conf)

logger.info("====== Notify End =======")