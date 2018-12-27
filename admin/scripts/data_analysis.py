import time
import re

from life.utils.process import (edit_mood, edit_mood_keywords, edit_consume, 
                                edit_time, edit_log, get_data, 
                                get_count, edit_consume_keywords, )
from life.utils.logger import Logger
from life.utils.analysis import (baidu_emotion, baidu_keywords, )
from life.utils.string import (wash_str, extract_zh, )


def thread_sleep(index):
    if index % 10 == 0:
        time.sleep(1)

def mood():
    count = get_count()
    end = 10
    while end <= count:
        #sleep
        thread_sleep(end)

        queryset = get_data(end-10, end)
        for q in queryset:
            washed_str = wash_str(q.log)

            try:
                mood = baidu_emotion(washed_str)['items'][0]['positive_prob']
            except:
                try:
                    zh_str = extract_zh(washed_str)
                    mood = baidu_emotion(zh_str)['items'][0]['positive_prob']
                except:
                    mood = 0.5
                

            edit_mood(q.pubtime, mood)

        end += 10


def mood_keywords():
    count = get_count()
    end = 10
    while end <= count:
        #sleep
        thread_sleep(end)
        
        queryset = get_data(end-10, end)
        for q in queryset:
            washed_str = wash_str(q.log)
            result = baidu_keywords(washed_str)
            mood_keywords = ''
            try:
                for item in result['items']:
                    mood_keywords += '%s%s ' % (item['prop'], item['adj'],)
            except:
                try:
                    zh_str = extract_zh(washed_str)
                    for item in result['items']:
                        mood_keywords += '%s%s ' % (item['prop'], item['adj'],)
                except:
                    pass

            edit_mood_keywords(q.pubtime, mood_keywords)

        end += 10
    
def consume():
    count = get_count()
    end = 10
    while end <= count:
        # sleep
        # thread_sleep(end) 

        queryset = get_data(end-10, end)
        for q in queryset:
            pubtime = q.pubtime
            raw_data = eval('[%s]' % q.consume)
            amount = 0.0
            consume_keywords_list = []

            for r in raw_data:
                amount += float(r['price'])
                consume_keywords_list.append(r['category'])

            consume_keywords = " ".join(set(consume_keywords_list))

            edit_consume_keywords(pubtime, amount, consume_keywords)

        end += 10

def run():
    pass
    # mood()
    # mood_keywords()
    # consume()
