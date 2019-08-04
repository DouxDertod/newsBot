# -*- coding: utf-8 -*-
import codecs

import os

from NewsModel import NewsDocument
import re
import requests
import datetime
import helper

appkey = '64ce0f495748e698'
url_GetCategory= 'https://api.jisuapi.com/news/channel'
url_GetNews='https://api.jisuapi.com/news/get'
# regex for fetch HTML TAG 用于匹配html tag
reg = re.compile('<[^>]*>')

num_maxNewsEachCategory=5000

def updateCategoryFile():
    categoryList =   getCategoryInfo()
    if not os.path.exists("tempfile"):
        os.makedirs("tempfile")
    f = codecs.open( 'tempfile/JiSuCategory.cat', "w", "utf-8")
    for category in categoryList:
        f.write(category+"\n")
    f.close()


def getCategoryInfo():
    params = dict(
        appkey=appkey
    )
    response = requests.get(url_GetCategory, params=params)
    return response.json()["result"]

def getNewsContent(category,start):
    params = dict(
        appkey=appkey,
        channel=category,
        num=40,
        start=start
    )
    response = requests.get(url_GetNews, params=params)

    return response.json()["result"]

def saveNewsEachCategory():
    f = codecs.open('tempfile/JiSuCategory.cat', "r", "utf-8")
    categories = f.readlines()
    for category in categories:
        saveServralNews(category)
    f.close()
def saveServralNews(category):

    try:
        count = 0
        page = 0
        while count < num_maxNewsEachCategory:
            start = page * 40
            newsList = getNewsContent(category, start)

            for news in newsList["list"]:
                if(count>=num_maxNewsEachCategory): return
                newsContent = reg.sub('', news["content"])
                newsContent = re.sub('(\s){2,}', ' ', newsContent).strip()
                if (newsContent.strip() == ""): continue
                length = newsContent.__len__()
                result = helper.count_from_str(newsContent)
                tags = []
                for k, v in result:
                    if v >= 5:
                        tags.append(k)


                newsDict={
                    "id": helper.generateId(),
                    "title":news["title"],
                    "content":newsContent,
                    "summary":newsContent,
                    "length":length,
                    "publish_time":helper.parseTime((news["time"][0:10])),
                    "archive_time":datetime.datetime.now(),
                    "author":news["url"],
                    "channel":news["src"],
                    "source":"JiSuShuJu",
                    "hot_value":0,
                    "category":[{"key":category.strip('\n'),"value":1}],
                    "tag":tags,
                    "position_city":None,
                    "position_province":None
                }
                nd = NewsDocument(newsDict)
                isExsit = nd.findByTitle();


                if isExsit:
                    return
                else:
                    nd.save()

                count+=1
            page += 1
    except Exception as ex:
        errorMessage=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S ")
        errorMessage+= category+"-No."+str(count)
        #errorMessage+=" error:"+ex.message
        print(errorMessage)
        if not os.path.exists("tempfile"):
            os.makedirs("tempfile")
        f = codecs.open('tempfile/JiSuErrorLog.log', "a", "utf-8")
        f.write(errorMessage)
        f.close()

