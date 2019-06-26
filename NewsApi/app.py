# -*- coding: utf-8 -*-
import json
from helper import json_resp
import flask
from flask import Flask, request
import NewsModel
app = Flask(__name__)
#
# @app.route("/")
# def index():
#     return "Flask App!"

@app.route("/news/query",methods = ['POST'])
def hello():
    # test ={
    #     "keyword":["飞机","炸弹"],
    #     "start_date":None,
    #     "end_date":None,
    #     "method":1,
    #     "exclude_keyword":[],
    #     "logic":1,
    #     "hot_value":-1
    #
    #        }
    data = request.data

    try:
        test =json.loads(data)
    except:

        return json_resp({'retcode': -1, 'msg': "Invalid JSON"})
    nm= NewsModel.NewsDocument()
    resultlist=nm.findByConditon(test)
    if(type(resultlist) == str):
        return json_resp({'retcode': -1, 'msg': resultlist})
    if resultlist=="[]" or resultlist.__len__()==0:
        return  json_resp({'retcode': -1, 'msg': "no records", 'data': ""})

    

    return  json_resp({'retcode': 0, 'msg': "success", 'data': resultlist})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=18088)