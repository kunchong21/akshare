#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/10/22 11:08
Desc: 腾讯-ticket数据
每3秒更新。延迟3~9秒
"""

import time
import pandas as pd
import requests




def stock_zh_a_ticket_tx_js_last(code:str = "sz000001",limit:int = 60) -> pd.DataFrame:

    """
    腾讯实时ticket
    https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2?
    code=sz300494&
    limit=60&
    direction=1&
    _callback=jQuery1124015866436473554701_1638978412407
    &_=1638978412408
    return ["成交时间", "成交价格", "价格变动", "成交量", "成交金额", "性质"]
    """


    url = " https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2"
    params = {
        "code": code,
        "limit": 60,
        "direction": "1",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params)
    text_data = r.text
    big_df = pd.DataFrame()
    temp_df = (pd.DataFrame(eval(text_data[text_data.find("["):text_data.find("]") + 1])).iloc[:, 0].str.split("\\\\/",
                                                                                                               expand=True))
    big_df = big_df.append(temp_df)


    if not big_df.empty:
        big_df = big_df.iloc[:, 1:]
        big_df.columns = ["成交时间", "成交价格", "价格变动", "成交量", "成交金额", "性质"]
        big_df.reset_index(drop=True, inplace=True)
        property_map = {
            "S": "卖盘",
            "B": "买盘",
            "M": "中性盘",
        }
        big_df["性质"] = big_df["性质"].map(property_map)
        big_df = big_df.astype({
            '成交时间': str,
            '成交价格': float,
            '价格变动': float,
            '成交量': int,
            '成交金额': int,
            '性质': str,
        })
    big_df['时间'] = big_df['成交时间'].str[0:5]
    # df.loc[df['name'] == '', 'x4'] = 0
    return big_df

def stock_zh_a_ticket_tx_js_last_current_date(code:str = "sz000001",limit:int = 60) -> pd.DataFrame:

    """
    腾讯分时数据
    https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2?
    code=sz300494&
    limit=60&
    direction=1&
    _callback=jQuery1124015866436473554701_1638978412407
    &_=1638978412408
    return ["成交时间", "成交价格", "价格变动", "成交量", "成交金额", "性质"]
    """


    url = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2"
    params = {
        "code": code,
        "limit": limit,
        "direction": "1",
        "_": int(time.time() * 1000),
    }
    r = requests.get(url, params=params)
    text_data = r.text
    dateNum = r.json()["data"]["date"]
    # print(r.json()["data"]["date"])
    big_df = pd.DataFrame()
    temp_df = (pd.DataFrame(eval(text_data[text_data.find("["):text_data.find("]") + 1])).iloc[:, 0].str.split("\\\\/",
                                                                                                               expand=True))
    big_df = big_df.append(temp_df)


    if not big_df.empty:
        big_df = big_df.iloc[:, 1:]
        big_df.columns = ["成交时间", "成交价格", "价格变动", "成交量", "成交金额", "性质"]
        big_df.reset_index(drop=True, inplace=True)
        property_map = {
            "S": "卖盘",
            "B": "买盘",
            "M": "中性盘",
        }
        big_df["性质"] = big_df["性质"].map(property_map)
        big_df = big_df.astype({
            '成交时间': str,
            '成交价格': float,
            '价格变动': float,
            '成交量': int,
            '成交金额': int,
            '性质': str,
        })
    big_df['时间'] = big_df['成交时间'].str[0:5]
    # df.loc[df['name'] == '', 'x4'] = 0
    return big_df

