import re
import random
import requests
import time
import uuid

from lxml import etree
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist

from life.base.models import (Data)
from life.utils.str_format import (str_to_md5str, )
from life.utils.analysis import baidu_emotion
from life.utils.logger import Logger

logger = Logger()
msg = 'SYNC %s < %s > SUCCESS!'


def save_data(pubtime, mood, consume, time, log):
    try:
        Data.objects.get(pubtime=pubtime)
    except ObjectDoesNotExist:
        Data(
            pubtime=pubtime, 
            mood=mood, 
            consume=consume,
            time=time,
            log=log,
        ).save()
        logger.record(msg % ('data', pubtime, ))

def data_exists(pubtime):
    try:
        return Data.objects.get(pubtime=pubtime)
    except ObjectDoesNotExist:
        return None
