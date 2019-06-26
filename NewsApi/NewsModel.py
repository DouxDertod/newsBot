# -*- coding: utf-8 -*-
import re
from pymongo import MongoClient
import json
from bson import ObjectId

import helper


class NewsModel(dict):

    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if not self._id:
            self.collection.insert(self)
        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def reload(self):
        if self._id:
            self.update(self.collection\
                    .find_one({"_id": ObjectId(self._id)}))

    def remove(self):
        if self._id:
            self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()

    def findByTitle(self):
        if self.title and self.publish_time:
            return self.collection.find_one({"title":self.title,"publish_time":self.publish_time})
        else:
            return "notitle"

    def findByConditon(self,conditionDict):

        queryDict = {"$and": []}
        if "keyword" in conditionDict and conditionDict["keyword"].__len__()>0:
            if  "logic" not in conditionDict:
                return "Require logic"
            if conditionDict["logic"] and conditionDict["logic"]==2:
                if "method" not in conditionDict:
                    return "Require method"
                keywordOrList = {"$or": []}
                for keyword in conditionDict["keyword"]:

                    if conditionDict["method"] == 1 :
                        keywordOrList["$or"].append({"title": {"$regex": keyword}})
                    elif conditionDict["method"] == 2:
                        keywordOrList["$or"].append({"content": {"$regex": keyword}})
                    elif conditionDict["method"] == 3:
                        keywordOrList["$or"].append({"content": {"$regex": keyword}})
                        keywordOrList["$or"].append({"title": {"$regex": keyword}})
                    else:
                        return "Invalid method"
                if keywordOrList["$or"].__len__() > 0:
                    queryDict["$and"].append(keywordOrList)

            elif conditionDict["logic"] and conditionDict["logic"]==1:
                if "method" not in conditionDict:
                    return "Require method"
                for keyword in  conditionDict["keyword"]:
                    keywordOrList = {"$or": []}
                    if conditionDict["method"] == 1 :
                        queryDict["$and"].append({"title":{"$regex":keyword}})
                    elif conditionDict["method"] == 2  :
                        queryDict["$and"].append({"content":{"$regex":keyword}})
                    elif conditionDict["method"] == 3:
                        queryDict["$and"].append({"$or": [{"title":{"$regex":keyword}},{"content":{"$regex":keyword}}]})
                    else:
                        return "Invalid method"
            else:
                return "Invalid logic"
        try:
            if "start_time"  in conditionDict and conditionDict["start_time"]!="":
                queryDict["$and"].append({"publish_time":{"$gt":helper.string2Datetime(conditionDict["start_time"])}})
        except:
            return "Invalid start time"
        try:
            if "end_time"  in conditionDict and conditionDict["end_time"]!="":
                queryDict["$and"].append({"publish_time":{"$lt":helper.string2Datetime(conditionDict["end_time"])}})
        except:
            return "Invalid end time"
        if "exclude_keyword"  in conditionDict  and conditionDict["exclude_keyword"].__len__()>0:
            if "method" not in conditionDict:
                return "Require method"

            for keyword in conditionDict["exclude_keyword"]:
                if conditionDict["method"] == 1 or conditionDict["method"]==3  :
                    queryDict["$and"].append({"title":{"$not":  re.compile(keyword)}})
                elif conditionDict["method"] == 2 or conditionDict["method"]==3 :
                    queryDict["$and"].append({"content": {"$not":  re.compile(keyword)}})
                else:
                    return "Invalid method"
        if "hot_value"  in conditionDict:
            queryDict["$and"].append({"hot_value": {"$gt":conditionDict["hot_value"]}})

        if "category"  in conditionDict:
            categoryOrList = {"$or":[]}
            for category in conditionDict["category"]:
                categoryOrList["$or"].append({"category":[{"key":category,"value":1}]})
            if categoryOrList["$or"].__len__()>0:
                queryDict["$and"].append(categoryOrList)
        if queryDict["$and"].__len__()==0:
            queryDict.pop("$and")
        skip=0

        limit=20
        if "limit" in conditionDict:
            limit=conditionDict["limit"]
            if limit>40 :limit=40
        if "page" in conditionDict:
            skip=conditionDict["page"]*limit
        result=[]
        print(json.dumps(queryDict))
        cursor=self.collection.find(queryDict).skip(skip).limit(limit)
        if "sort_name" in conditionDict:
            if "sort_order" in conditionDict and conditionDict["sort_order"]=="ASC":
                cursor.sort(conditionDict["sort_name"])
            elif "sort_order" in conditionDict and conditionDict["sort_order"]=="DESC":
                cursor.sort(conditionDict["sort_name"],-1)
            else:
                return "Invalid Sort Order"
        for record in cursor:
            record.pop("_id")
            try:
                record["publish_time"]=helper.datetime2String(record["publish_time"])
            except:
                record["publish_time"]=""

            try:
                record["archive_time"] = helper.datetime2String(record["archive_time"])
            except:
                record["archive_time"]=""
            result.append(record)

        return result


class NewsDocument(NewsModel):
    client = MongoClient('localhost', 27017)
    collection = client["news-db-001"]["newsTable"]

    @property
    def keywords(self):
        return self.title.split()
