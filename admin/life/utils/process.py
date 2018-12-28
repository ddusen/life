import re
import random
import requests
import time
import uuid

from lxml import etree
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist

from life.base.models import (Data)
from life.utils.analysis import baidu_emotion
from life.utils.logger import Logger

logger = Logger()
msg_s = 'SYNC %s < %s > SUCCESS!'
msg_f = 'SYNC %s < %s > FAIL!（已存在）'
msg_e = 'EDIT %s < %s > SUCCESS!'


def save_data(pubtime, mood=-1, mood_keywords='', consume=0.0, consume_keywords='', time_keywords='', consume_log='', time_log='', event_log=''):
    try:
        Data.objects.get(pubtime=pubtime)
        logger.record(msg_f % ('DATA', pubtime, ))
    except ObjectDoesNotExist:
        Data(
            pubtime=pubtime, 
            mood=mood, 
            mood_keywords=mood_keywords,
            consume=consume,
            consume_keywords=consume_keywords,
            time_keywords=time_keywords,
            consume_log=consume_log,
            time_log=time_log,
            event_log=event_log,
        ).save()
        logger.record(msg_s % ('data', pubtime, ))

def edit_mood(pubtime, mood):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.mood = mood
        data_obj.save()
        logger.record(msg_e % ('DATA(mood)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, mood=mood)

def edit_mood_keywords(pubtime, mood_keywords):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.mood_keywords = mood_keywords
        data_obj.save()
        logger.record(msg_e % ('DATA(mood_keywords)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, mood_keywords=mood_keywords)

def edit_consume_keywords(pubtime, amount, consume_keywords):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.consume = amount
        data_obj.consume_keywords = consume_keywords
        data_obj.save()
        logger.record(msg_e % ('DATA(amount, consume_keywords)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, consume=amount, consume_keywords=consume_keywords)

def edit_consume_log(pubtime, consume_log):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.consume_log = '''%s%s''' % (data_obj.consume_log, consume_log, )
        data_obj.save()
        logger.record(msg_e % ('DATA(consume_log)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, consume_log=consume_log)

def edit_time_log(pubtime, time_log):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.time_log = time_log
        data_obj.save()
        logger.record(msg_e % ('DATA(time_log)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, time_log=time_log)

def edit_event_log(pubtime, event_log):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.event_log = event_log
        data_obj.save()
        logger.record(msg_e % ('DATA(event_log)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, event_log=event_log)

def get_count():
    return Data.objects.count()

def get_data(start, end):
    return Data.objects.filter(pubtime__gte='2017-12-31').order_by('-pubtime')[start:end:]

def data_exists(pubtime):
    try:
        return Data.objects.get(pubtime=pubtime)
    except ObjectDoesNotExist:
        return None
        