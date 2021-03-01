# -*- coding: utf-8 -*-
"""
a sample to show how to utilize the realtime watching function
"""

import xalpha as xa
import pandas as pd

# first introduce some aim you want to watch
# you must use rfundinfo instead of standard fundinfo class to get the realtime netvalue
GTRY_JunGong = xa.rfundinfo("001838")
HTF_XinNengYuanCar = xa.rfundinfo("501057")
ZhO_YiLiao = xa.rfundinfo("003095")
FG_HuGangShen = xa.rfundinfo("005847")

XQ_HeRun = xa.rfundinfo("163406")
ZhO_XinLanChou = xa.rfundinfo("166002")
FG_TianHui = xa.rfundinfo("161005")
YFD_LanChou = xa.rfundinfo("005827")
ND_ZhouQiCeLue = xa.rfundinfo("570008")

# secondly setup some policies you want to run and watch
# 定期不定额的定投策略
# 2021/2/27: 以日为单位，净值1.9以下5倍定投，净值2.07以下3倍定投，净值2.2以下2倍定投，2.21以上不再定投，中间正常定投

DQbuDE_GTRY_JunGong = xa.policy.scheduled_tune(
    GTRY_JunGong, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.1820, 2),(1.2476, 1)]) 

DQbuDE_XinNengYuanCar = xa.policy.scheduled_tune(
    HTF_XinNengYuanCar, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.9819, 2),(2.0920, 1)]) 

DQbuDE_ZhO_YiLiao = xa.policy.scheduled_tune(
    ZhO_YiLiao, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(3.2107, 2),(3,3890, 1)]) 

DQbuDE_FG_HuGangShen = xa.policy.scheduled_tune(
    FG_HuGangShen, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(2.1351, 2),(2.2537, 1)]) 

# 主动混合
DQbuDE_XQ_HeRun = xa.policy.scheduled_tune(
    XQ_HeRun, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.9295, 2),(2.0367, 1)]) 

DQbuDE_ZhO_XinLanChou = xa.policy.scheduled_tune(
    ZhO_XinLanChou, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(2.1961, 2),(2.3181, 1)]) 

DQbuDE_FG_TianHui = xa.policy.scheduled_tune(
    FG_TianHui, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(3.5102, 2),(3.7052, 1)]) 

DQbuDE_YFD_LanChou = xa.policy.scheduled_tune(
    YFD_LanChou, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(2.8958, 2),(3.0567, 1)]) 

DQbuDE_ND_ZhouQiCeLue = xa.policy.scheduled_tune(
    ND_ZhouQiCeLue, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(3.7037, 2),(3.9094, 1)]) 

check = xa.review([DQbuDE_GTRY_JunGong, DQbuDE_XinNengYuanCar, DQbuDE_ZhO_YiLiao, DQbuDE_FG_HuGangShen, 
    DQbuDE_XQ_HeRun, DQbuDE_ZhO_XinLanChou, DQbuDE_FG_TianHui, DQbuDE_YFD_LanChou, DQbuDE_ND_ZhouQiCeLue], 
    ["《定期不定额 - 题材 - 军工》", "《定期不定额 - 题材 - 新能源车》", "《定期不定额 - 题材 - 医疗》", "《定期不定额 - 题材 - 港股》",
    "《定期不定额 - 主动混合 - 兴全和润》", "《定期不定额 - 主动混合 - 中欧新蓝筹》", "《定期不定额 - 主动混合 - 富国天惠》", "《定期不定额 - 主动混合 - 易方达蓝筹》"], "《定期不定额 - 主动混合 - 诺德周期策略》"])

""" WG_XinNengYuanCar = xa.policy.grid(
    yhXinNengYuanCar,
    [5,5,5,5,5],
    [6,10,10,10,10],
    '2021-01-01', '2021-07-31', 
    totmoney=10000)

WG_XinNengYuanCar.sellpts,WG_XinNengYuanCar.buypts

# thirdly put all your favorite policies into a review class and name these policies correspondingly
check = xa.review([DQbuDE_XinNengYuanCar,WG_XinNengYuanCar], ["《定期不定额 - 题材 - 新能源车》","《网格 - 题材 - 新能源车》"]) """

# fourthly, setup the email configuration dict
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

# you are all done

"""
关于如何将该脚本定时运行，就不是 xalpha 所关心的问题了，您可以选取系统依赖的定时方案。比如 *nix 中的 crontab 等，将
｀python3 notification.py｀ 加入系统定时任务即可，建议每个工作日15:00前运行。需要提前预留出程序运行，邮件发送与接受，基金购买的时间。
一旦超过 15:00 则成为下一交易日的申购赎回。
"""
