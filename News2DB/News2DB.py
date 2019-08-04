# -*- coding: utf-8 -*-
import datetime
import threading
import JiSuShuJu as jssj
import helper


def  recordNews():
    helper.updateStopWordsFile()
    jssj.updateCategoryFile()
    jssj.saveNewsEachCategory()

    getNextTime()



def getNextTime():
    # 获取现在时间
    now_time = datetime.datetime.now()
    # 获取2小时后时间
    next_time = now_time+ datetime.timedelta(hours=+2)


    # 获取距离2小时候时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    print(timer_start_time)

    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time,  recordNews)
    timer.start()

def main():
    # 获取现在时间
    now_time = datetime.datetime.now()
    # 获取下次时间
    next_time = now_time
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day


    next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 11:49:00", "%Y-%m-%d %H:%M:%S")



    # 获取距离时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()


    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, recordNews)
    timer.start()





main();

