#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/8/12 17:03
Desc: 东方财富网-数据中心-F10
https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/Index?type=web&code=SH600519#
"""
from tqdm import tqdm

import pandas as pd
import requests


def stock_gsgg(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-公司高管列表
    https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/Index?type=web&code=SH600519#glcjj-0
    :param symbol: 股票代码
    :type symbol: str
    :return: 高管列表
    :rtype: pandas.DataFrame
    """

    url = "https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/PageAjax"
    params = {"code": symbol}

    r = requests.get(url, params=params)
    data_json = r.json()
    gglb_df = pd.DataFrame(data_json["gglb"])

    gglb_df.columns = [
        "全局代码",
        "市场代码",
        "姓名",
        "职务",
        "PERSON_CODE",
        "持股数",
        "薪酬",
        "POSITION_TYPE_CODE",
        "性别",
        "学历",
        "年龄",
        "简介",
        "任职时间",
        "IS_COMPARE",
    ]

    gglb_df = gglb_df[
        [
            "全局代码",
            "市场代码",
            "姓名",
            "职务",
            "持股数",
            "薪酬",
            "性别",
            "学历",
            "年龄",
            "简介",
            "任职时间",
        ]
    ]
    return gglb_df


if __name__ == "__main__":
    stock_gsgg_df = stock_gsgg(symbol="SH600519")
    print(stock_gsgg_df.to_html())
