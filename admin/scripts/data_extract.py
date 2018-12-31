import time
import re

from life.utils.process import (edit_mood, edit_consume_log, edit_time_log, 
                                edit_event_log, )
from life.utils.logger import Logger

def thread_sleep(index):
    if index % 10 == 0:
        time.sleep(1)

#处理每日时间消费信息
def data_time_log():
    with open('/mnt/f/downloads/time_log.enex','r') as f:
        raw_data = f.read()
        title_pattern = re.compile(r'<title>(......)</title>')
        title_list = title_pattern.findall(raw_data)
        content_pattern = re.compile(r'<en-note>(.*?)</en-note>')
        content_list = content_pattern.findall(raw_data)
        
        for index, content in enumerate(content_list):
            #sleep
            thread_sleep(index)

            title = title_list[index]
            pubtime = '20%s-%s-%s' % (title[0:2], title[2:4], title[4:6], )
            edit_time_log(pubtime, content)

#处理每日金钱消费信息
def data_consume_log():
    index = 0
    with open('/mnt/f/downloads/DailyCost.csv','r') as f:
        raw_data = f.readline()
        while raw_data:
            index+=1
            # 不读取文件第一行数据
            if index == 1:
                raw_data = f.readline()
                continue
            #sleep
            thread_sleep(index)
            
            data_list = raw_data.strip().split(',')
            pubtime = data_list[0]
            consume = '''{'category':'%s', 'price':'%s', 'detail':'%s'},''' % (data_list[2], data_list[3], data_list[6])
            edit_consume_log(pubtime, consume)

            raw_data = f.readline()

#处理每日日志信息
def data_event_log():
    index = 0
    with open('/mnt/f/downloads/mood_log.html','r') as f:
        raw_data = f.read()
        title_pattern = re.compile(r'<h1>(......)</h1>')
        title_list = title_pattern.findall(raw_data)
        content_pattern = re.compile(r'</h1>([\s\S]*?)<hr>')
        content_list = content_pattern.findall(raw_data)
        for index, title in enumerate(title_list):
            #sleep
            thread_sleep(index)

            content = content_list[index]
            pubtime = '20%s-%s-%s' % (title[0:2], title[2:4], title[4:6], )
            edit_event_log(pubtime, content)

def run():
    data_time_log()
    data_consume_log()
    data_event_log()