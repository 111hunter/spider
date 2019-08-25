from utils.Log import Log

import urllib.parse
from datetime import datetime
import time

def do_fix_time():
    now = datetime.now()
    nowHour = now.hour
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    if nowHour >= 23 or nowHour < 6:
        time.sleep(60)
        return nowTime,True
    return None,False

def urldeocde(str):
    return urllib.parse.unquote(str)

def check(target, log):
    if not target:
        Log.e(log)
        return False
    return True

def formatDate(date):
    return datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
