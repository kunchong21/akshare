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


def stock_f10_gbjg(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-f10
    https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/Index?type=web&code=SH600519#glcjj-0
    :param symbol: 股票代码
    :type symbol: str
    :return: 股本构成
    :rtype: pandas.DataFrame
    """

    url = "https://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/PageAjax"
    params = {"code": symbol}

    r = requests.get(url, params=params)
    data_json = r.json()
    gbjg_df = pd.DataFrame(data_json["gbjg"])
    #xsjj 限售解禁，gbgc 股本构成 ,gbjg 股本结构，lngbbd 历年股本变动

    gbjg_df.columns = [
        "全局代码",
        "市场代码",
        "未流通股份",
        "流通受限股份",
        "已流通股份",
        "总股本",
        "已上市流通A股",
        "已上市流通B股",
        "境外上市流通股",
        "其它已流通股份",
        "未流通股份-占比",
        "流通受限股份-占比",
        "已流通股份-占比",
        "总股本-占比",
        "已上市流通A股-占比",
        "已上市流通B股-占比",
        "境外上市流通股-占比",
        "其它已流通股份-占比",
        "流通股份合计-占比"
    ]

    return gbjg_df


def stock_f10_lngbbd(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-f10
    https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/Index?type=web&code=SH600519#glcjj-0
    :param symbol: 股票代码
    :type symbol: str
    :return:  历年股本变动
    :rtype: pandas.DataFrame
    """

    url = "https://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/PageAjax"
    params = {"code": symbol}

    r = requests.get(url, params=params)
    data_json = r.json()
    #xsjj 限售解禁，gbgc 股本构成 ,gbjg 股本结构，lngbbd 历年股本变动

    lngbbd_df = pd.DataFrame(data_json["lngbbd"])
    lngbbd_df.columns = [
        "全局代码",
        "市场代码",
        "时间",
        "总股本",
         "流通受限股份",
        "其他内资持股(受限)",
        "境内自然人持股(受限)",
        "国有法人持股(受限)",
        "LIMITED_OVERSEAS_NOSTATE",
        "LIMITED_OVERSEAS_NATURAL",
        "已流通股份	",
        "已上市流通A股	",
        "已上市流通B股",
        "境外上市流通股",
        "流通A股",
        "受限流通A股",
        "未流通股份",
        "未流通B股",
        "OTHER_FREE_SHARES",
        "国家持股(受限)	",
        "其他内资持股(受限)	",
        "锁定股",
        "受限外资股",
        "受限港股",
        "发起人股份	",
        "国有法人持股	",
        "自然人持股	",
        "募集法人股	",
        "募集国家持股",
        "募集内资股",
        "募集海外股",
        "变动原因"
    ]

    return lngbbd_df



if __name__ == "__main__":
    stock_gsgg_df = stock_f10_gbjg(symbol="SH600519")
    print(stock_gsgg_df.to_html())

    stock_f10_lngbbd_df = stock_f10_lngbbd("sh600519")
    print(stock_f10_lngbbd_df.to_csv())