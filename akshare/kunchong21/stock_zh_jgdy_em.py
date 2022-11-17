import json
import os
import re
import time

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

from akshare.utils import demjson
from bs4 import BeautifulSoup

def stock_zh_jgdy_detail_em(symbol: str = "301029",date_time:str = "2022-11-10") -> pd.DataFrame:
    """
    机构调研具体内容
    https://data.eastmoney.com/jgdy/dyxx/301029,2022-11-10.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 城市映射
    :rtype: pandas.DataFrame
    """
    url="https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        # "callback": "jQuery1123014935097377281648_1668598316150",
        "reportName": "RPT_ORG_SURVEY",
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,NOTICE_DATE,RECEIVE_START_DATE,RECEIVE_END_DATE,RECEIVE_OBJECT,RECEIVE_PLACE,RECEIVE_WAY_EXPLAIN,INVESTIGATORS,RECEPTIONIST,NUM,CONTENT,ORG_TYPE",
        # "quoteColumns": ,
        "source": "WEB",
        "client": "WEB",
        "sortColumns": "NUMBERNEW",
        "sortTypes": 1,
        "filter": '(IS_SOURCE="1")(SECURITY_CODE="'+symbol+'")(RECEIVE_START_DATE=\''+date_time+'\')',
        "_" : int(time.time() * 1000),
    }
    print(params.get("filter"))
    r = requests.get(url,params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])



    # del temp_df["降序"]
    # temp_df.reset_index(inplace=True)
    # temp_df["index"] = temp_df.index + 1
    # temp_df.columns = ["序号", "省份", "城市", "AQI", "空气质量", "PM2.5浓度", "首要污染物"]
    # temp_df["AQI"] = pd.to_numeric(temp_df["AQI"])
    return temp_df

if __name__ == '__main__':
    stock_zh_jgdy_detail_em_df = stock_zh_jgdy_detail_em();
    # print(stock_zh_jgdy_detail_em_df.to_csv())
    print(stock_zh_jgdy_detail_em_df)

