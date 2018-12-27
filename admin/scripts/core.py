import time
import re

from life.utils.process import (edit_mood, edit_consume, edit_time, 
                                edit_log, )
from life.utils.logger import Logger

def thread_sleep(index):
    if index % 10 == 0:
        time.sleep(1)

#处理每日时间消费信息
def data_time():
    with open('/home/sdu/Downloads/time-log.enex','r') as f:
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
            edit_time(pubtime, content)

#处理每日金钱消费信息
def data_consume():
    index = 0
    with open('/home/sdu/Downloads/DailyCost.csv','r') as f:
        raw_data = f.readline()
        while raw_data:
            index+=1
            #sleep
            thread_sleep(index)
            
            data_list = raw_data.strip().split(',')
            pubtime = data_list[0]
            consume = '''{'category':'%s', 'amount':'%s', 'detail':'%s'}''' % (data_list[2], data_list[3], data_list[6])
            edit_consume(pubtime, consume)

def run():
    data_time()
    data_consume()