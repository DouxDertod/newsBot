# -*- coding: utf-8 -*-
import codecs
import json

import time
import random
import datetime
from collections import Counter
import jieba.analyse
import jieba
import os
import requests
url_GetStopWords = "https://account-center-test.chewrobot.com/api/v1/news/words/invalids"

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
            date=nowdate+datetime.timedelta(minutes=-30)
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

def updateStopWordsFile():
    StopWords =   json.loads( getStopWords())
    f = codecs.open( 'stop.txt', "w", "utf-8")
    for StopWord in StopWords:
        f.write(StopWord+"\n")
    f.close()

def getStopWords():

    response = requests.get(url_GetStopWords)
    return response.json()["payload"]

