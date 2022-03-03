from datetime import datetime, date, timedelta
import time
import math


class METHODTYPE:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'


def get_nowTime():
    now = datetime.now().strftime("%Y-%m-%d")
    return now


# get_passed_days t2 = "2020-05-05" , t1 is now_day
def get_days(t1, t2):
    time1 = t1.split("-")
    time2 = t2.split("-")
    date1 = date(int(time1[0]), int(time1[1]), int(time1[2]))
    date2 = date(int(time2[0]), int(time2[1]), int(time2[2]))
    return date1.__sub__(date2).days


def get_detail_time():
    now = datetime.now()
    return str(now).split(".")[0]


def get_date(time_str):
    return datetime.strptime(time_str, '%b-%d-%Y %H:%M:%S')


def get_delay_time(delay_time):
    day = date.today()
    now = datetime.now()
    delta = timedelta(days=delay_time)
    n_days_after = now + delta
    return n_days_after.strftime('%Y-%m-%d %H:%M:%S')
