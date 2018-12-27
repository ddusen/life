import time
import re

from life.utils.process import (edit_mood,edit_keywords, edit_consume, 
                                edit_time, edit_log, get_log, 
                                get_count, )
from life.utils.logger import Logger
from life.utils.analysis import (baidu_emotion, baidu_keywords, )
from life.utils.string import (wash_str, extract_zh, )

def thread_sleep(index):
    if index % 10 == 0:
        time.sleep(1)

def mood():
    count = get_count()
    end = 10
    while end < count:
        #sleep
        thread_sleep(end)

        queryset = get_log(end-10, end)
        for q in queryset:
            washed_str = wash_str(q.log)

            try:
                mood = baidu_emotion(washed_str)['items'][0]['positive_prob']
            except:
                try:
                    zh_str = extract_zh(washed_str)
                    mood = baidu_emotion(zh_str)['items'][0]['positive_prob']
                except Exception as e:
                    mood = 0.5
                

            edit_mood(q.pubtime, mood)

        end += 10


def keywords():
    count = get_count()
    end = 10
    while end < count:
        #sleep
        thread_sleep(end)
        
        queryset = get_log(end-10, end)
        for q in queryset:
            zh_str = extract_zh(q.log)
            result = baidu_keywords(zh_str)
            keywords = ''
            try:
                for item in result['items']:
                    keywords += '%s%s ' % (item['prop'], item['adj'],)
            except:
                pass

            edit_keywords(q.pubtime, keywords)

        end += 10
    

def run():
    mood()
    keywords()
