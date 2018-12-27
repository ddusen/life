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


def save_data(pubtime, mood=-1, consume='', time='', log=''):
    try:
        Data.objects.get(pubtime=pubtime)
        logger.record(msg_f % ('DATA', pubtime, ))
    except ObjectDoesNotExist:
        Data(
            pubtime=pubtime, 
            mood=mood, 
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
        save_data(pubtime, mood, '', '', '')

def edit_consume(pubtime, consume):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.consume = '''%s%s''' % (data_obj.consume, consume, )
        data_obj.save()
        logger.record(msg_e % ('DATA(consume)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime, -1, consume, '', '')

def edit_time(pubtime, time):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.time = time
        data_obj.save()
        logger.record(msg_e % ('DATA(time)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime, -1, '', time, '')

def edit_log(pubtime, log):
    try:
        data_obj = Data.objects.get(pubtime=pubtime)
        data_obj.log = log
        data_obj.save()
        logger.record(msg_e % ('DATA(log)', pubtime, ))
    except ObjectDoesNotExist:
        save_data(pubtime, -1, '', '', log)

def get_count():
    return Data.objects.count()

def get_log(start, length=10):
    return Data.objects.order_by('pubtime')[start::length]

def data_exists(pubtime):
    try:
        return Data.objects.get(pubtime=pubtime)
    except ObjectDoesNotExist:
        return None
        