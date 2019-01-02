import re
import hashlib


def str_to_md5str(raw_str):
    hash_md5 = hashlib.md5(raw_str.encode('utf-8'))
    return hash_md5.hexdigest()


#提取字符串中中文
def extract_zh(raw_str):
    return ','.join(re.compile("[\u4e00-\u9fa5]+").findall(raw_str))
    
#清洗字串(过滤表情,过滤非标准空格)
def wash_str(raw_str):
    try:
        str_re = re.compile('[\U00010000-\U0010ffff]')
    except re.error:
        str_re = re.compile('[\uD800-\uDBFF][\uDC00-\uDFFF]')
    new_str = str_re.sub('', raw_str)
    new_str = new_str.replace('\xa0', '').replace('\u2615', '').replace('\ufe0f', '').replace('\u2044', '')
    return new_str

#计算总时间
def calculate_time(d_dict, key, value):
    pattern_1 = re.compile(r'(\d+)点半')
    pattern_2 = re.compile(r'(\d+)分钟')
    pattern_3 = re.compile(r'(\d+)小时')
    pattern_4 = re.compile(r'(\d+)点(\d+)')
    pattern_5 = re.compile(r'(\d+)点')
    pattern_6 = re.compile(r'(\d+)个半小时')

    temp = 0
    if pattern_1.findall(value):
        temp = (float(pattern_1.findall(value)[0]) + 0.5) * 60
    elif pattern_2.findall(value):
        temp = float(pattern_2.findall(value)[0])
    elif pattern_3.findall(value):
        temp = float(pattern_3.findall(value)[0]) * 60
    elif pattern_4.findall(value):
        hours, minute = pattern_4.findall(value)[0]
        temp = float(hours) * 60 + float(minute)
    elif pattern_5.findall(value):
        temp = float(pattern_5.findall(value)[0]) * 60
    elif pattern_6.findall(value):
        temp = (float(pattern_6.findall(value)[0]) + 0.5 ) * 60
    temp = 24*60-temp if temp > 16*60 else temp
    return d_dict[key] + temp if d_dict.get(key) else temp

# 格式化
def calculate_time_format(d_dict):
    formated_dict = {}
    amount = 0
    for k, v in d_dict.items():
        amount += v
        formated_dict[k] = round(v/60, 1)
    formated_dict['Blank'] = round(0 if 24*60-amount < 0 else (24*60-amount)/60, 1)
    return formated_dict

# 消费 english to chinese
def consume_en_to_zh(key):
    en_to_zh = {
            'General': '一般',
            'Food': '餐饮',
            'Drinks': '饮料',
            'Groceries': '水果',
            'Shopping': '购物',
            'Personal': '个人',
            'Entertail': '娱乐',
            'Movies': '电影',
            'Social': '社交',
            'Transport': '交通',
            'App Store': 'App',
            'Mobile': '通讯',
            'Computer': '电脑',
            'Gifts': '礼品',
            'Housing': '房租',
            'Travel': '旅行',
            'Tickets': '门票',
            'Books': '书籍',
            'Medical': '医疗',
            'Transter': '转账',
    }
    return '其它' if not en_to_zh.get(key) else en_to_zh[key]

# 时间使用 english to Chinese
def time_en_to_zh(key):
    en_to_zh = {
        'Study': '学习',
        'Coding': '工作',
        'Fitness': '健身',
        'Eat':  '餐饮',
        'Sleep': '睡眠',
        'Entertainment': '娱乐',
        'Walk': '行走',
        'Others': '其它',
        'Blank': '空白',
    }
    return '其它' if not en_to_zh.get(key) else en_to_zh[key]
