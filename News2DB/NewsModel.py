# -*- coding: utf-8 -*-

from pymongo import MongoClient

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
        if self.title and self.author:
            return self.collection.find_one({"title":self.title,"author":self.author})
        else:
            return "notitle"

    def findByConditon(self,conditionDict):
        queryDict = {"$and": []}
        if conditionDict.has_key("keyword") and conditionDict["keyword"].__len__()>0:
            if not conditionDict.has_key("logic"):
                return "Require logic"
            if conditionDict["logic"] and conditionDict["logic"]==2:
                pass
            if conditionDict["logic"] and conditionDict["logic"]==1:
                if not conditionDict.has_key("method"):
                    return "Require method"
                for keyword in  conditionDict["keyword"]:

                    if conditionDict["method"] == 1 or conditionDict["method"]==3 :
                        queryDict["$and"].append({"title":{"$regex":keyword}})
                    elif conditionDict["method"] == 2 or conditionDict["method"]==3 :
                        queryDict["$and"].append({"content":{"$regex":keyword}})
                    else:
                        return "Invalid method"
            else:
                return "Invalid logic"
        try:
            if conditionDict.has_key("start_time") and conditionDict["start_time"]!="":
                queryDict["$and"].append({"publish_time":{"$gt":helper.string2Datetime(conditionDict["start_time"])}})
        except:
            return "Invalid start time"
        try:
            if conditionDict.has_key("end_time") and conditionDict["end_time"]!="":
                queryDict["$and"].append({"publish_time":{"$lt":helper.string2Datetime(conditionDict["end_time"])}})
        except:
            return "Invalid end time"
        if conditionDict.has_key("exclude_keyword") and conditionDict["exclude_keyword"].__len__()>0:
            if not conditionDict.has_key("method"):
                return "Require method"
            for keyword in conditionDict["keyword"]:
                if conditionDict["method"] == 1 or conditionDict["method"] == 3:
                    queryDict["$and"].append({"title": {"$regex": keyword}})
                elif conditionDict["method"] == 2 or conditionDict["method"] == 3:
                    queryDict["$and"].append({"content": {"$regex": keyword}})
                else:
                    return "Invalid method"
        if  conditionDict.has_key("hot_value"):
            queryDict["$and"].append({"hot_value": {"$gt":conditionDict["hot_value"]}})

        skip=0

        limit=20
        if conditionDict.has_key("limit"):
            limit=conditionDict["limit"]
            if limit>40 :limit=40
        if conditionDict.has_key("page"):
            skip=conditionDict["page"]*limit
        result=[]
        cursor=self.collection.find(queryDict).skip(skip).limit(limit)
        if conditionDict.has_key("sort_name"):
            if conditionDict.has_key("sort_order")and conditionDict["sort_order"]=="ASC":
                cursor.sort(conditionDict["sort_name"])
            elif  conditionDict.has_key("sort_order")and conditionDict["sort_order"]=="DESC":
                cursor.sort(conditionDict["sort_name"],-1)
            else:
                return "Invalid Sort Order"
        for record in cursor:
            record.pop("_id")
            record["publish_time"]=helper.datetime2String(record["publish_time"])
            record["archive_time"] = helper.datetime2String(record["archive_time"])
            result.append(record)

        return result

    def findAllRecord(self):
        cursor = self.collection.find()
        return cursor

    def deduplication(self):
        cursor = self.findAllRecord()
        for record in cursor:
            result =self.collection.find({"title": self.title, "author": self.author, "id": {"$ne": record["id"]}})
            if result:
                self.collection.remove(record)
            if record["summary"]!=record["content"]:
                self.update(record)

class NewsDocument(NewsModel):
    client = MongoClient('localhost', 27017)
    collection = client["news-db-001"]["newsTable"]

    @property
    def keywords(self):
        return self.title.split()