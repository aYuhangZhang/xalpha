# -*- coding: utf-8 -*-
"""
a sample to show how to utilize the realtime watching function
"""

import xalpha as xa
import pandas as pd

# first introduce some aim you want to watch
# you must use rfundinfo instead of standard fundinfo class to get the realtime netvalue

rf_HTF_XinNengYuanCar = xa.rfundinfo("501057")  # 汇添富新能源车
rf_GTRY_JunGong = xa.rfundinfo("001838")     # 国投瑞银军工
rf_FG_HuGangShen = xa.rfundinfo("005847")  # 富国沪港深
rf_XQ_HeRun = xa.rfundinfo("163406")     # 兴全和润
rf_FG_TianHui = xa.rfundinfo("161005")   # 富国天惠
rf_YFD_LanChou = xa.rfundinfo("005827")  # 易方达蓝筹精选
rf_ZhO_YiLiang = xa.rfundinfo("003095")  # 中欧医疗健康
rf_ZhO_XinLanChou = xa.rfundinfo("166002")   # 中欧新蓝筹
rf_GT_Nasdaq100 = xa.rfundinfo("160213")  # 国泰纳斯达克100
rf_YFD_ZhongGaiHuLian = xa.rfundinfo("006327")  # 易方达中概互联


# secondly setup some policies you want to run and watch
# 定期不定额的定投策略
# 2021/2/27: 以日为单位，净值1.9以下5倍定投，净值2.07以下3倍定投，净值2.2以下2倍定投，2.21以上不再定投，中间正常定投
cl_HTF_XinNengYuanCar = xa.policy.scheduled_tune(
    rf_HTF_XinNengYuanCar, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.7617, 4),(1.8718, 3),(1.8719, 1)]) 

cl_JunGong = xa.policy.scheduled_tune(
    rf_GTRY_JunGong, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.0506, 4),(1.1163, 3),(1.1164, 1)]) 

cl_FG_HuGangShen = xa.policy.scheduled_tune(
    rf_FG_HuGangShen, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.8947, 4),(2.0165, 3),(2.0166, 1)]) 

cl_XQ_HeRun = xa.policy.scheduled_tune(
    rf_XQ_HeRun, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.9295, 2),(2.0367, 1.1),(2.0368, 1)]) 

cl_FG_TianHui = xa.policy.scheduled_tune(
    rf_FG_TianHui, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(3.5102, 2),(3.7052, 1.1),(3.7053, 1)]) 



# thirdly put all your favorite policies into a review class and name these policies correspondingly
check = xa.review([cl_HTF_XinNengYuanCar, cl_JunGong, cl_FG_HuGangShen, cl_XQ_HeRun, cl_FG_TianHui], 
                ["新能源车-定期不定额", "国投瑞银军工-定期不定额", "富国沪港深-定期不定额", "兴全和润-定期不定额", "富国天惠-定期不定额"])

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
