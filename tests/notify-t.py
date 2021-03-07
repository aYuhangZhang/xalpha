# -*- coding: utf-8 -*-

import sys
from loguru import logger

sys.path.insert(0, "../")
import xalpha as xa
import pandas as pd

logger.add('notifyFund.txt', format="{time} {level} {message}")
logger.info("====== Notify Start =======")


fundNum = ["001838", "501057", "166002"]
fundName = ["《题材 - 军工》", "《题材 - 新能源车》", "<中欧蓝筹混合>"]

# fundNum = ["001838", "501057", "003095"]
# fundName = ["《题材 - 军工》", "《题材 - 新能源车》", "《题材 - 医疗》"]

n = 0

downPercent = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
down_fund = [0] * len(downPercent)
DQbuDE_policy_lst = [''] * len(fundNum)
# DQbuDE_policy_lst = ['', '', '', '', '', '', '', '', '']

def get_mul_targetPrice(fundNum):
    path = "fund2021.csv"
    read = xa.record(path) 

    bankstate = read.status

    # bankstate.to_csv("d:\\tmp\\test-record.csv", encoding='utf_8_sig')
    # logger.debug("========== Record status ==============" + str(read.status))

    transaction_record = bankstate[bankstate[fundNum]!=0.0]
    # transaction_record = bankstate["date", fundNum]     wrong

    transaction_record = transaction_record.loc[:, ['date', fundNum]]

    logger.debug("=========== fund buy record :" + fundNum + '\n' + str(transaction_record))

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
for k in range(0, len(fundName)):
    print("DQbuDE_policy_lst" + str(k) +":======" + str(DQbuDE_policy_lst[k]))

check = xa.review([DQbuDE_policy_lst[0],DQbuDE_policy_lst[1],DQbuDE_policy_lst[2]], 
    [fundName[0],fundName[1],fundName[2]])

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