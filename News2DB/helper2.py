# -*- coding: utf-8 -*-
import calendar
import codecs
from datetime import date
import json
import time
import random
import datetime
from collections import Counter

import jieba
from flask import make_response
def generateId():
    now_time = datetime.datetime.now()
    timestamp = time.mktime(now_time.timetuple())
    return '001'+'J01'+str(int(timestamp))+str(random.randint(1000,9999))

def parseTime(datastr):
    try:
        datastr+=" 12:00:00"
        date = datetime.datetime.strptime(datastr, "%Y-%m-%d %H:%M:%S")
        nowdate = datetime.datetime.now()
        if date.year == nowdate.year and date.month==nowdate.month and date.day==nowdate.day:
            date=nowdate
            date=nowdate+datetime.timedelta(minutes=-3)
        return date
    except:
        return None

def getPresentTime():
    now_time = datetime.datetime.now();
    return str(now_time.year).zfill(4)+"-"+str(now_time.month).zfill(2)+"-"+str(now_time.day).zfill(2)+" "+str(now_time.hour).zfill(2)+":"+str(now_time.minute).zfill(2)+":"+str(now_time.second).zfill(2)

def datetime2String(target_date):
    return str(target_date.year).zfill(4) + "-" + str(target_date.month).zfill(2) + "-" + str(target_date.day).zfill(
        2) + " " + str(target_date.hour).zfill(2) + ":" + str(target_date.minute).zfill(2) + ":" + str(target_date.second).zfill(
        2)
def string2Datetime(target_str):
    return datetime.datetime.strptime(target_str, "%Y-%m-%d %H:%M:%S")
#
# def encode_datetime(obj):
#     """
#     编码时间格式
#     :param obj:时间对象
#     :return:年月日格式时间
#     """
#     if isinstance(obj, date):
#         return obj.strftime('%Y-%m-%d')
#     raise TypeError(repr(obj) + ' is not JSON serializable')
#
#
# class DateTimeEncoder(json.JSONEncoder):
#     """
#     时间编辑器
#     """
#     def default(self, o):
#         if isinstance(o, datetime.datetime):
#             return calendar.timegm(o.utctimetuple()) * 1000 + o.microsecond/1000
#         elif isinstance(o, date):
#             return o.strftime('%Y-%m-%d')
#
#         else:
#             return json.JSONEncoder.default(self, o)

def json_resp(obj, status=200, retcode=0):
    """
    json格式回复
    :param obj:
    :param status:
    :param retcode:
    :return:
    """
    if 'retcode' not in obj:
        obj['retcode'] = retcode
    if 'status' not in obj:
        obj['status'] = status
    resp = make_response(json.dumps(obj, ensure_ascii=False).encode('utf8'), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def stopwordslist(filepath):
    with codecs.open(filepath, 'r', 'utf-8') as f:

        stopwords = [line.strip() for line in  f.readlines()]
    return stopwords



def count_from_str(content, top_limit=0):
    if top_limit <= 0:
        top_limit = 100
    tags = jieba.analyse.extract_tags(content, top_limit)

    words = jieba.cut(content)
    counter = Counter()

    stopwords = stopwordslist('stop.txt')  # 加载停用词
    for word in words:
        if word.isdigit():
            continue;
        if word not in stopwords:
            if word in tags:
                counter[word] += 1

    return counter.most_common(top_limit)
