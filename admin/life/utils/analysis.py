'''
    中文语义分析
'''
import json
import requests
import random

from aip import AipNlp


# baidu 文章标签
def baidu_keywords(my_str):
    text = repr(my_str.encode("GBK"))[1::]

    """ 你的 APPID AK SK """
    key = {
        'APP_ID': '11140757', 
        'API_KEY': 'xP5tsjqUn4uEMOxCHCXb2HTO', 
        'SECRET_KEY': 'M9lxojP8dRoeEGp4wU74AQNLW2RQdD9v', 
    }

    client = AipNlp(key['APP_ID'], key['API_KEY'], key['SECRET_KEY'])

    """ 如果有可选参数 """
    options = {}
    options["type"] = '8'
    print(text)
    print(type(text))
    """ 带参数调用评论观点抽取 """
    return client.commentTag(text, options)


# BosonNLP 中文情感分析
def boson_emotion(my_str):

    SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis?weibo'

    headers = {'X-Token': 'kOOze9uF.9476.mEQLFUou6dqs'}

    data = json.dumps(my_str)
    resp = requests.post(
        SENTIMENT_URL,
        headers=headers,
        data=data.encode('utf-8')
    )

    return resp.json()


# baidu 中文情感分析
def baidu_emotion(my_str):
    """ 你的 APPID AK SK """
    key1 = {
        'APP_ID': '10801558', 
        'API_KEY': 'FCUZBiFKi4MZO4WnpzU5XeG9', 
        'SECRET_KEY': 't9IVKaYsQzosWwh9EugqBLXmb78P5ei7', 
    }
    key2 = { 
        'APP_ID': '10801769', 
        'API_KEY': 'IsfNeTsr4Y6osB910RmGiKuG', 
        'SECRET_KEY': 'li2NoLMtZi5rUDkrbwGz1z1IR2xhfxyW',
    }
    key3 = {
        'APP_ID': '10862510', 
        'API_KEY': 'QjIRtECSCVrgAGh5AxU63u4Z', 
        'SECRET_KEY': 'iheVvaZqSFSfwtQFkXcQtt0P056RECuU',
    }

    cur_key = random.choice([key1, key2, key3])
    
    client = AipNlp(cur_key['APP_ID'], cur_key['API_KEY'], cur_key['SECRET_KEY'])
    '''
    response result like this:
    {
    "text":"苹果是一家伟大的公司",
    "items":[
        {
            "sentiment":2,    //表示情感极性分类结果
            "confidence":0.40, //表示分类的置信度
            "positive_prob":0.73, //表示属于积极类别的概率
            "negative_prob":0.27  //表示属于消极类别的概率
        }
    ]
    }
    '''

    return client.sentimentClassify(my_str)
