# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/5/13 19:25
Desc: 东方财富网-数据中心-公告大全-沪深 A 股公告
http://data.eastmoney.com/notices/hsa/5.html
"""
from datetime import datetime
import json
import random
import time

import pandas as pd
import requests
from tqdm import tqdm

def stock_notice_report_sse_now()->pd.DataFrame:
    """
    上交所公告
    http://www.sse.com.cn/disclosure/listedinfo/announcement/
    实时。当天的公告
    :return: 上交所 A 股公告
    :rtype: pandas.DataFrame
    """
    url = "http://www.sse.com.cn/disclosure/listedinfo/announcement/json/stock_bulletin_publish_order.json"
    params = {
        "v": random.random()
    }
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["publishData"])
    temp_df.columns = [
        "_",
        "公告日期",
        "公告标题",
        "公告类型",
        "公告时间",
        "公告链接",
        "股票代码",
        "股票名称",
        "-",
    ]
    temp_df = temp_df[
        [
            "公告日期",
            "公告标题",
            "公告类型",
            "公告时间",
            "公告链接",
            "股票代码",
            "股票名称",
        ]
    ]
    temp_df["公告链接"] = "https://static.sse.com.cn/"+temp_df["公告链接"]
    return temp_df

def stock_notice_report_szse(start_date:str="",end_date:str = "")->pd.DataFrame:
    """
    深交所公告
    http://www.szse.cn/disclosure/listed/notice/index.html
    实时。当天的公告
    :param start_date %Y-%m-%d %H:%M:%S or %Y-%m-%d 默认当天时间
    :type start_date str
    :param end_date %Y-%m-%d %H:%M:%S or %Y-%m-%d 默认当前时间
    :type end_date str
    :return: 深交所 A 股公告
    :rtype: pandas.DataFrame
    """
    if start_date == "":
        start_date = time.strftime("%Y-%m-%d", time.localtime())
    if end_date == "":
        end_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    url = "http://www.szse.cn/api/disc/announcement/annList?random="+str(random.random)
    params = {"seDate":[start_date,end_date],
              "channelCode":["listedNotice_disc"],
              "pageSize":50,
              "pageNum":1
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "80",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "www.szse.cn",
        "Origin": "http://www.szse.cn",
        "Referer": "http://www.szse.cn/disclosure/listed/notice/index.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "X-Request-Type": "ajax",
        "X-Requested-With": "XMLHttpRequest",
    }
    string = json.dumps(params)
    r = requests.post(url, data=string, headers=headers)

    data_json = r.json()
    print(data_json)
    announceCount = data_json["announceCount"]
    if announceCount == 0 :
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"])
    for i,data in temp_df.iterrows():
        temp_df.loc[i,"secCode"] = (",".join(data["secCode"]))
        temp_df.loc[i, "secName"] = (",".join(data["secName"]))
    temp_df.columns = [
        "id",
        "公告ID",
        "公告标题",
        "content",
        "发布时间",
        "公告文件链接",
        "公告文件类型",
        "公告大小",
        "股票代码",
        "股票名称",
        "bondType",
        "bigIndustryCode",
        "bigCategoryId",
        "smallCategoryId",
        "channelCode",
        "-",
    ]
    temp_df = temp_df[
        [
            "id",
            "公告ID",
            "公告标题",
            "发布时间",
            "公告文件链接",
            "公告文件类型",
            "公告大小",
            "股票代码",
            "股票名称",
        ]


    ]
    temp_df["公告文件链接"] = "http://disc.static.szse.cn"+temp_df["公告文件链接"]
    temp_df["来源页面"] = "http://www.szse.cn/disclosure/listed/bulletinDetail/index.html?" + temp_df["id"]
    return temp_df

def stock_notice_report_bse(start_date:str="",end_date:str = "")->pd.DataFrame:
    """
    北交所公告
    http://www.bse.cn/disclosure/announcement.html
    实时，默认为当天内的公告
    :param start_date %Y-%m-%d %H:%M:%S or %Y-%m-%d 默认当天时间
    :type start_date str
    :param end_date %Y-%m-%d %H:%M:%S or %Y-%m-%d 默认当天
    :type end_date str
    :return: 深交所 A 股公告
    :rtype: pandas.DataFrame
    """
    if start_date == "":
        start_date = time.strftime("%Y-%m-%d", time.localtime())
        if end_date == "":
            end_date = time.strftime("%Y-%m-%d", time.localtime())

    # page = 1
    # url = "http://www.bse.cn/disclosureInfoController/infoResult_zh.do"
    url = "http://www.bse.cn/disclosureInfoController/infoResult_zh.do?callback=jQuery331_"+str((int)(time.time()))

    params = [
        "disclosureType%5B%5D=5",
        "disclosureSubtype%5B%5D=",
        "page=",
        "companyCd=",
        "isNewThree=1",
        "startTime="+start_date,
        "endTime="+end_date,
        "keyword=",
        "xxfcbj%5B%5D= 2",
        "needFields%5B%5D=companyCd",
        "needFields%5B%5D=companyName",
        "needFields%5B%5D=disclosureTitle",
        "needFields%5B%5D=disclosurePostTitle",
        "needFields%5B%5D=destFilePath",
        "needFields%5B%5D=publishDate",
        "needFields%5B%5D=xxfcbj",
        "needFields%5B%5D=destFilePath",
        "needFields%5B%5D=fileExt",
        "needFields%5B%5D=xxzrlx",
        "sortfield=xxssdq",
        "sorttype=asc"
    ]
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "Hm_lvt_ef6193a308904a92936b38108b93bd7f=1668412171; Hm_lpvt_ef6193a308904a92936b38108b93bd7f=1668412386",
        "DNT": "1",
        "Host": "www.bse.cn",
        "Origin": "http://www.bse.cn",
        "Referer": "http://www.bse.cn/disclosure/announcement.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    data_string = "&".join(params);
    r = requests.post(url,data=data_string,headers=headers)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{"): -2])
    content_list = json_data["listInfo"]["content"]
    total_page = json_data["listInfo"]["totalPages"]
    print(text_data)
    # announceCount = data_json["announceCount"]
    # if announceCount == 0 :
    #     return pd.DataFrame()

    big_df = pd.DataFrame()
    for page in tqdm(range(0, total_page + 1), leave=False):
        params = [
            "disclosureType%5B%5D=5",
            "disclosureSubtype%5B%5D=",
            "page=" + str(page),
            "companyCd=",
            "isNewThree=1",
            "startTime=" + start_date,
            "endTime=" + end_date,
            "keyword=",
            "xxfcbj%5B%5D= 2",
            "needFields%5B%5D=companyCd",
            "needFields%5B%5D=companyName",
            "needFields%5B%5D=disclosureTitle",
            "needFields%5B%5D=disclosurePostTitle",
            "needFields%5B%5D=destFilePath",
            "needFields%5B%5D=publishDate",
            "needFields%5B%5D=xxfcbj",
            "needFields%5B%5D=destFilePath",
            "needFields%5B%5D=fileExt",
            "needFields%5B%5D=xxzrlx",
            "sortfield=xxssdq",
            "sorttype=asc"
        ]
        data_string = "&".join(params);
        r = requests.post(url, data=data_string, headers=headers)
        text_data = r.text
        json_data = json.loads(text_data[text_data.find("{"): -2])
        content_list = json_data["listInfo"]["content"]
        big_df = pd.concat([big_df,  pd.DataFrame(content_list)], ignore_index=True)


    print(big_df)
    big_df.columns = [
        "股票代码",
        "股票名称",
        "公告文件链接",
        "disclosurePostTitle",
        "公告标题",
        "公告文件类型",
        "发布时间",
        "xxfcbj",
        "xxzrlx"
    ]
    big_df = big_df[
        [
        "股票代码",
        "股票名称",
        "公告文件链接",
        "公告标题",
        "公告文件类型",
        "发布时间",
        ]
    ]

    big_df["公告文件链接"] = "http://www.bse.cn"+big_df["公告文件链接"]
    # temp_df["来源页面"] = "http://www.szse.cn/disclosure/listed/bulletinDetail/index.html?" + temp_df["id"]
    return big_df



if __name__ == "__main__":

    stock_notice_report_szse = stock_notice_report_szse()
    print(stock_notice_report_szse)

    stock_notice_report_detail_now = stock_notice_report_sse_now()
    stock_notice_report_detail_now.to_csv("/app/sse_report.csv")
    print(stock_notice_report_detail_now)

    stock_notice_report_bse_df = stock_notice_report_bse(start_date="2022-11-01")
    print(stock_notice_report_bse_df)
    print(stock_notice_report_bse_df.to_html())
