import datetime
import re

import pandas as pd
import requests
from py_mini_racer import py_mini_racer
from tqdm import tqdm

from akshare.bond.cons import (
    zh_sina_bond_hs_cov_count_url,
    zh_sina_bond_hs_cov_payload,
    zh_sina_bond_hs_cov_url,
    zh_sina_bond_hs_cov_hist_url,
)
from akshare.stock.cons import hk_js_decode
from akshare.utils import demjson



def bond_zh_hs_real() -> pd.DataFrame:
    """
    新浪财经-债券-沪深可转债的实时行情数据; 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 所有沪深可转债在当前时刻的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_bond_hs_cov_page_count()
    zh_sina_bond_hs_payload_copy = zh_sina_bond_hs_cov_payload.copy()
    for page in tqdm(range(1, page_count + 1), leave=False):
        zh_sina_bond_hs_payload_copy.update({"page": page})
        zh_sina_bond_hs_payload_copy.update({"sort": "amount"})
        zh_sina_bond_hs_payload_copy.update({"asc": "0"})
        zh_sina_bond_hs_payload_copy.update({"_s_r_a": "sort"})
        res = requests.get(
            zh_sina_bond_hs_cov_url, params=zh_sina_bond_hs_payload_copy
        )
        data_json = demjson.decode(res.text)
        big_df = pd.concat(
            [big_df, pd.DataFrame(data_json)], ignore_index=True
        )
    return big_df

def _get_zh_bond_hs_cov_page_count() -> int:
    """
    新浪财经-行情中心-债券-沪深可转债的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 总页数
    :rtype: int
    """
    params = {
        "node": "hskzz_z",
    }
    r = requests.get(zh_sina_bond_hs_cov_count_url, params=params)
    page_count = int(re.findall(re.compile(r"\d+"), r.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1
