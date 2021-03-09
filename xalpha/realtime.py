# -*- coding: utf-8 -*-
"""
module for realtime watch and notfication
"""
# deprecated
# 该模块与现在的主线进展关系不大，可用性不强，
# xalpha 不应过度干涉通知或可能的自动交易部分
# 因此该模块可能随时不再支持

import datetime as dt
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from re import match
from xalpha.universal import _get_daily
from numpy.lib.function_base import append
import pandas as pd
from pandas.core.base import DataError

from xalpha.cons import today_obj, rget
from xalpha.info import fundinfo
from xalpha.trade import trade

import sys
import xalpha as xa
from loguru import logger
sys.path.insert(0, "../")

def check_duplicate_buy(fundNum, date, rf_target_price, price_scope_max, price_scope_min):
    path = "..\\tests\\fund2021.csv"
    i = 0
    compare_result = ["", ""]

    # bank_state = pd.read_csv(path)
    # buy_record = bank_state(fundNum)
    # logger.debug(fundName + "的购买记录" + str(buy_record))
    read = xa.record(path)
    bankstate = read.status

    # date日期格式化yyyymmdd
    date = date.date()
    logger.debug("===========格式化后的date" + str(date))

    # 从账单中获取fundNum的有效购买记录 获取 >0 的数据 去除 <=0 的数据
    transaction_record = bankstate[bankstate[fundNum] > 0.0]
    # transaction_record = bankstate["date", fundNum]     wrong

    transaction_record = transaction_record.loc[:, ['date', fundNum]]
    logger.debug("=========== fund buy record :" + fundNum + str(transaction_record))

    history_price_list = []
    min_history_price = 0

    # 通过账单获取所有历史交易的的日期和金额
    for i in range(0,len(transaction_record)):        
        history_transaction_date = transaction_record.iloc[i, -2]
        history_transaction_date = history_transaction_date.date()
        history_transaction_money = transaction_record.iloc[i, -1]
        history_transaction_money = int(history_transaction_money)
        logger.debug("===============曾经购买日期：" + str(history_transaction_date) + "===曾经购买金额：" + str(history_transaction_money))

        # 获取历史交易净值
        history_price_df = xa.get_daily(('F'+str(fundNum)), start=str(history_transaction_date), end=str(history_transaction_date))
        logger.debug("==================history_price dataframe = "+"\n" + str(history_price_df))

        history_price = history_price_df.iloc[0, -1]
        history_price_date = history_price_df.iloc[0, -2]
        logger.debug("==================history_price = " + str(history_price) + "===日期：" + str(history_price_date))

        history_price_list.append([str(history_price)])
        
        logger.debug("===============历史购买时的净值：" + str(history_price) + "净值高限=" + str(price_scope_max) + "净值底限 = " + str(price_scope_min))

        if (price_scope_min <= history_price <= price_scope_max):
            if (history_price > rf_target_price):
                logger.debug(str(fundNum) + "比较结果：已在同一点大于现净值加过")
                compare_result.append([(" 大于 " + str(history_transaction_date)), str(history_transaction_money)])
            else:
                logger.debug(str(fundNum) + "比较结果：已在同一点小于现净值加过")

                # 当前净值与历史净值相差的百分比
                lss_percent = (history_price - rf_target_price)/history_price

                # 小数转化为百分比显示
                lss_percent = "%.2f%%" % (lss_percent * 100)
                logger.debug("==========lss_percent = " + str(lss_percent))

                compare_result.append([(" 小于 " + str(history_transaction_date)), (str(history_transaction_money) + "估算幅度" +str(lss_percent))])

    # 打印 history_price_list
    logger.debug("=========history_price_list: " + str(history_price_list))


    # 获取20210113到今天的历史净值 date close
    all_history_price_df = xa.get_daily(('F'+str(fundNum)), start="20210113", end=str(date))
    logger.debug("get_daily========start=20210113=========== end = " + "\n" + str(date))

    # 去除date数据,为取min准备
    all_history_price_df = all_history_price_df.loc[:,"close"]
    logger.debug("========= all_history_price_df:" + str(all_history_price_df))

    all_history_lowest_price = all_history_price_df.min()
    logger.debug("========= all_history_lowest_price:" + str(all_history_lowest_price))

    if (rf_target_price < all_history_lowest_price):
        # 当前新低净值 与 历史净值相差的百分比
        min_history_price = min(history_price_list)
        # 列表转化为float
        min_history_price = list(map(float, min_history_price))
        # 列表取值
        min_history_price = min_history_price[0]

        logger.debug("======= min_history_price: " + str(min_history_price))
        # 计算历史最低交易降幅
        least_percent = (rf_target_price - min_history_price)/min_history_price
        least_percent = "%.2f%%" % (least_percent * 100)
        logger.debug("======= least_percent: " + str(least_percent))

        compare_result.append([("==已超过历史最低价:" + str(all_history_lowest_price)) , ("历史最低交易降幅：" + str(least_percent))])


    logger.debug("============comparesult " + str(compare_result))
    return str(compare_result)



        #else:
            #logger.debug("===============历史购买时的净值：" + str(history_price) + "净值高限=" + str(price_scope_max) + "净值底限 = " + str(price_scope_min))
            #logger.debug( str(i) + "次比较结果：不在范围内，可加仓")

       
            
    # read = xa.record(path) 
    # read.status
    # sysopen = xa.mul( status = read.status ) 
    # df = sysopen.combsummary()
    # df_fund_cost = df.loc[df['基金代码']==fundNum, ['单位成本']]
  

    # oriNetValue_fund = df_fund_cost.iloc[-1, -1]

    # for i in range(0,len(downPercent)):
    #     down_fund[i] = round((oriNetValue_fund - oriNetValue_fund * downPercent[i]), 4)

    #     print("downPercent" +str(i)+ " = " +str(downPercent[i]))
    #     print("down_fund"+str(i)+" = " + str(down_fund[i]))



def _format_addr(s):
    """
    parse the email sender and receiver, Chinese encode and support

    :param s: eg. 'name <email@website.com>, name2 <email2@web2.com>'
    """
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def mail(
    title,
    content,
    sender=None,
    receiver=None,
    password=None,
    server=None,
    port=None,
    sender_name="sender",
    receiver_name=None,
):
    """
    send email

    :param title: str, title of the email
    :param content: str, content of the email, plain text only
    :param conf: all other paramters can be import as a dictionay, eg.conf = {'sender': 'aaa@bb.com',
        'sender_name':'name', 'receiver':['aaa@bb.com','ccc@dd.com'], 'password':'123456',
        'server':'smtp.bb.com','port':123, 'receiver_name':['me','guest']}.
        The receiver_name and sender_name options can be omitted.
    """
    ret = True
    try:
        if receiver_name is None:
            receiver_name = ["receiver" for _ in receiver]
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = _format_addr("%s <%s>" % (sender_name, sender))
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        receivestr = ""
        for i, s in enumerate(receiver):
            receivestr += receiver_name[i]
            receivestr += " <"
            receivestr += s
            receivestr += ">, "
        msg["To"] = _format_addr(receivestr)  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg["Subject"] = title  # 邮件的主题，即标题

        server = smtplib.SMTP_SSL(server, port)  # 发件人邮箱中的SMTP服务器和端口号
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(
            sender, receiver, msg.as_string()
        )  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
    except Exception:
        ret = False
    return ret


class rtdata:
    """
    get real time data of specific funds

    :param code: string of six digitals for funds
    """

    def __init__(self, code):
        url = "http://fundgz.1234567.com.cn/js/" + code + ".js"
        page = rget(url)
        self.code = code
        self.rtvalue = float(match(r'.*"gsz":"(\d*\.\d*)",.*', page.text)[1])
        self.name = match(r'.*"name":"([^,]*)",.*', page.text)[1]
        self.time = dt.datetime.strptime(
            match(r'.*"gztime":"([\d\s\-\:]*)".*', page.text)[1], "%Y-%m-%d %H:%M"
        )


def rfundinfo(
    code, round_label=0, dividend_label=0, fetch=False, save=False, path="", form="csv"
):
    """
    give a fundinfo object with todays estimate netvalue at running time

    :param code: string of six digitals for funds
    :param fetch: boolean, when open the fetch option, info class will try fetching from local files first in the init
    :param save: boolean, when open the save option, info classes automatically save the class to files
    :param path: string, the file path prefix of IO
    :param form: string, the format of IO, options including: 'csv'
    :returns: the fundinfo object
    """
    fundobj = fundinfo(
        code,
        round_label=round_label,
        dividend_label=dividend_label,
        fetch=fetch,
        save=save,
        path=path,
        form=form,
    )
    rt = rtdata(code)
    rtdate = dt.datetime.combine(rt.time, dt.time.min)
    rtvalue = rt.rtvalue
    if (rtdate - fundobj.price.iloc[-1].date).days > 0:
        fundobj.price = fundobj.price.append(
            pd.DataFrame(
                [[rtdate, rtvalue, fundobj.price.iloc[-1].totvalue, 0]],
                columns=["date", "netvalue", "totvalue", "comment"],
            ),
            ignore_index=True,
        )
    return fundobj


class review:
    """
    review policys and give the realtime purchase suggestions

    :param policylist: list of policy object
    :param namelist: list of names of corresponding policy, default as 0 to n-1
    :param date: object of datetime, check date, today is prefered, date other than is not guaranteed
    """

    def __init__(self, policylist, namelist=None, date=today_obj()):
        self.warn = []
        self.message = []
        self.policylist = policylist
        if namelist is None:
            self.namelist = [i for i in range(len(policylist))]
        else:
            self.namelist = namelist
        assert len(self.policylist) == len(self.namelist)

        PRICE_UP = 0.05
        PRICE_DOWN = 0.05

        print("================ realtime")   #yh debug
        for i, policy in enumerate(policylist):
            row = policy.status[policy.status["date"] == date]
            # logger.debug("=========row: " + "\n" + str(row).strip())
            # logger.debug("=============date:" + str(date))
            if len(row) == 1:
                warn = (
                    policy.aim.name,
                    policy.aim.code,
                    row.iloc[0].loc[policy.aim.code],
                    self.namelist[i],
                )
                self.warn.append(warn)
                print("================ " + str(warn[0]) + str(warn[2]))   # yh debug    
                if warn[2] > 0:
                    sug = "买入%s元" % warn[2]

                    # ======= yh check duplicate transaction start ==========

                    rf_target_fund = xa.get_rt('F'+str(warn[1]))
                    # rf_target_fund = rfundinfo(str(warn[1]))
                    
                    rf_target_price = rf_target_fund.get('estimate')
                    rf_target_price_datetime = rf_target_fund.get('estimate_time')

                    rf_target_price = round(rf_target_price, 4)
                    
                    logger.debug(str(date) + "================ " + str(warn[0]) + "基金净值price：" + str(rf_target_price) + "=== 日期："+ str(rf_target_price_datetime))

                    price_scope_max = round(rf_target_price + rf_target_price * PRICE_UP, 4)
                    price_scope_min = round(rf_target_price - rf_target_price * PRICE_DOWN, 4)
                    logger.debug("=========== price_scope_max = " + str(price_scope_max) + "=========== price_scope_min = " + str(price_scope_min))

                    compare_result = check_duplicate_buy(str(warn[1]), date, rf_target_price, price_scope_max, price_scope_min)

                    if (compare_result != ["", ""]):
                        logger.debug("比较结果：已在同一点加过" + str(compare_result))
                        sug = sug + "！注！已在同一点加过 " + str(compare_result) + "=== 上限：" + str("%.2f%%" % (PRICE_UP * 100)) + "; 下限：-" + str("%.2f%%" % (PRICE_DOWN * 100)) + "==="
                        logger.debug("============sug = " + sug)
                        
                    # ======= yh check duplicate transaction end ==========

                elif warn[2] < 0:
                    ratio = -warn[2] / 0.005 * 100
                    share = (
                        trade(fundinfo(warn[1]), policy.status)
                        .briefdailyreport()
                        .get("currentshare", 0)
                    )
                    share = -warn[2] / 0.005 * share
                    sug = "卖出%s%%的份额，也即%s份额" % (ratio, share)
                self.message.append(
                    "根据%s计划，建议%s，%s(%s)" % (warn[3], sug, warn[0], warn[1])
                )
        self.content = "\n".join(map(str, self.message))

    def __str__(self):
        return self.content

    def notification(self, conf):
        """
        send email of self.content, at least support for qq email sender

        :param conf: the configuration dictionary for email send settings, no ** before the dict in needed.
            eg.conf = {'sender': 'aaa@bb.com',
            'sender_name':'name', 'receiver':['aaa@bb.com','ccc@dd.com'], 'password':'123456',
            'server':'smtp.bb.com','port':123, 'receiver_name':['me','guest']}.
            The receiver_name and sender_name options can be omitted.
        """
        if self.content:
            ret = mail("Notification", self.content, **conf)
            if ret:
                print("邮件发送成功")
            else:
                print("邮件发送失败")
        else:
            print("没有提醒待发送")
