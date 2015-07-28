# !/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import time

# 类型转换异常
class DatetimeConvertError(Exception):
    def __init__(self, value=''):
        self.error_msg = "Cann't convert %s to datetime type." % value ;

    def __str__(self):
        return repr(self.error_msg) ;


# 获取当前系统时间
def now():
    return datetime.now() ;


# 计算两个时间差,精确到微秒
def diff_mseconds(start_time, finish_time):
    return (finish_time - start_time) ;


# 给某个时间加上一个时间间隔(天为单位),正数外后推,负数往前
def add_days(now, interval):
    if isinstance(now, str):
        now = str_to_datetime(now) ;
    return now + timedelta(days=interval) ;


# 比较两个时间的先后,大于返回1,小于返回-1,相等返回0
def compare(first, second):
    if not isinstance(first, datetime):
        first = str_to_datetime(first) ;
    if not isinstance(second, datetime):
        second = str_to_datetime(second) ;
    value = 0 ;
    if first > second:
        value = 1 ;
    elif first < second:
        value = -1 ;
    return value ;


# 将字符串转换为时间
def str_to_datetime(datetime_str):
    try:
        pos = datetime_str.find(':') + 1 ;
        if datetime_str.find(':', pos) == -1:
            datetime_str += ':00' ;
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S') ;
    except:
        raise DatetimeConvertError(datetime_str) ;


if __name__ == '__main__':
    '''start_time = now();
    time.sleep(5);
    finish_time = now();
    print diff_mseconds(start_time, finish_time);'''
    #print str_to_datetime('2013-1-10 00:00:00');
    print str_to_datetime(u'2013-1-10 00:00:00')