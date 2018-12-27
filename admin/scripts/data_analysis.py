import time
import re

from life.utils.process import (edit_mood, edit_consume, edit_time, 
                                edit_log, get_log, get_count, )
from life.utils.logger import Logger
from life.utils.analysis import baidu_emotion
from life.utils.string import wash_str

def thread_sleep(index):
    if index % 10 == 0:
        time.sleep(1)

def mood():
    count = get_count()
    end = 10
    while end < count:
        queryset = get_log(end-10, end)
        for q in queryset:
            washed_str = wash_str(q.log)

            try:
                mood = baidu_emotion(washed_str)['items'][0]['positive_prob']
            except:
                mood = 0.5

            edit_mood(q.pubtime, mood)

        end += 10

def run():
    mood()
