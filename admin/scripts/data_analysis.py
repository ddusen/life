import time
import re

from life.utils.process import (edit_mood, edit_consume, edit_time, 
                                edit_log, get_log, get_count, )
from life.utils.logger import Logger
from life.utils.analysis import baidu_emotion
from life.utils.string import filter_emoji

def thread_sleep(index):
    if index % 10 == 0:
        time.sleep(1)

def mood():
    count = get_count()
    start = 0
    while start < count:
        queryset = get_log(start)
        for q in queryset:
            washed_str = filter_emoji(q.log)
            mood = baidu_emotion(washed_str)
            print(mood)

        i = 10 / 0

        start += 10

def run():
    mood()
