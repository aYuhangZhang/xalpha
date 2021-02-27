# -*- coding: utf-8 -*-
"""
a sample to show how to utilize the realtime watching function
"""

import xalpha as xa
import pandas as pd

# first introduce some aim you want to watch
# you must use rfundinfo instead of standard fundinfo class to get the realtime netvalue
yhXinNengYuanCar = xa.fundinfo("501057")

# secondly setup some policies you want to run and watch
# 定期不定额的定投策略
# 2021/2/27: 以日为单位，净值1.9以下5倍定投，净值2.07以下3倍定投，净值2.2以下2倍定投，2.21以上不再定投，中间正常定投
cl_XinNengYuanCar = xa.policy.scheduled_tune(
    yhXinNengYuanCar, 
    500, 
    times=pd.date_range('2021-01-01','2021-07-01',freq='D'),
    piece=[(1.9, 5),(2.07, 3),(2.2, 2),(2.21,1)]) 



# thirdly put all your favorite policies into a review class and name these policies correspondingly
check = xa.review([cl_XinNengYuanCar], ["变路虎"])

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
