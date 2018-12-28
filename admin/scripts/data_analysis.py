import time
import re

from life.utils.process import (edit_mood, edit_mood_keywords, get_count,
                                get_data, edit_consume_keywords, edit_time_keywords, )
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
            washed_str = wash_str(q.event_log)

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
            washed_str = wash_str(q.event_log)
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
            raw_data = eval('[%s]' % q.consume_log)
            amount = 0.0
            consume_keywords_list = []

            for r in raw_data:
                amount += float(r['price'])
                consume_keywords_list.append(r['category'])

            consume_keywords = " ".join(set(consume_keywords_list))

            edit_consume_keywords(pubtime, amount, consume_keywords)

        end += 10

def time_keywords():
    corpus = {
        'Study': ['学', '复习', '读', '研'],
        'Coding': ['工作', '制作', 'coding'],
        'Fitness': ['锻炼', '羽毛球'],
        'Eat': ['饭', '菜'],
        'Sleep': ['休'],
        'Entertainment': ['娱乐'],
        'Walk': ['路', '走'],
        'Others': [],
    }
    result = {}
    count = get_count()
    end = 10
    while end <= count:
        # sleep
        # thread_sleep(end) 

        queryset = get_data(end-10, end)
        for q in queryset:
            pubtime = q.pubtime
            raw_data = q.time_log

            item_list = re.compile(r'<div>(.*?)</div>').findall(raw_data)

            for index, item in item_list[1:-1:]:

                def inner():
                    try:
                        name, content = item.split('：')
                    except:
                        name, content = item.split(':')
                    for key, values in corpus.items()
                        for value in values:
                            if name.find(value) > -1:
                                # calculate_time()
                                return

                inner()
            # edit_time_keywords(pubtime, time_keywords)

        end += 10

def run():
    # mood()
    # mood_keywords()
    # consume()
    time_keywords()
