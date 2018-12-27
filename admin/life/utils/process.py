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


def save_data(pubtime, mood=-1, keywords='', consume='', time='', log=''):
    try:
        Data.objects.get(pubtime=pubtime)
        logger.record(msg_f % ('DATA', pubtime, ))
    except ObjectDoesNotExist:
        Data(
            pubtime=pubtime, 
            mood=mood, 
            keywords=keywords,
            consume=consume,
            time=time,
            log=log,
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

def edit_keywords(pubtime, keywords):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.keywords = keywords
        data_obj.save()
        logger.record(msg_e % ('DATA(keywords)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, keywords=keywords)

def edit_consume(pubtime, consume):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.consume = '''%s%s''' % (data_obj.consume, consume, )
        data_obj.save()
        logger.record(msg_e % ('DATA(consume)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, consume=consume)

def edit_time(pubtime, time):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.time = time
        data_obj.save()
        logger.record(msg_e % ('DATA(time)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, time=time)

def edit_log(pubtime, log):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.log = log
        data_obj.save()
        logger.record(msg_e % ('DATA(log)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime=pubtime, log=log)

def get_count():
    return Data.objects.count()

def get_log(start, end):
    return Data.objects.order_by('pubtime')[start:end:]

def data_exists(pubtime):
    try:
        return Data.objects.get(pubtime=pubtime)
    except ObjectDoesNotExist:
        return None
        