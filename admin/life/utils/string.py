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
    pattern_1 = re.compile(r'(.*?)点半')
    pattern_2 = re.compile(r'(..)分钟')
    pattern_3 = re.compile(r'(.)小时')
    pattern_4 = re.compile(r'(..)点(..)')
    pattern_5 = re.compile(r'(..)点')
    pattern_6 = re.compile(r'(.)个半小时')

    temp = 0
    if pattern_1.findall(value):
        temp = (float(pattern_1.findall(value)[0]) + 0.5) * 60
    elif pattern_2.findall(value):
        temp = float(pattern_2.findall(value)[0])
    elif pattern_3.findall(value):
        temp = float(pattern_3.findall(value)[0]) * 60
    elif pattern_4.findall(value):
        hours, minute = pattern_4.findall(value)[0]
        temp = (24 - float(hours)) * 60 - float(minute)
    elif pattern_5.findall(value):
        hours = float(pattern_5.findall(value))
        temp = (hours if hours < 16 else 24-hours) * 60
    elif pattern_6.findall(value):
        temp = (float(pattern_6.findall(value)) + 0.5 ) * 60

    return d_dict[key] + temp if d_dict.get(key) else temp

# 格式化字符串
def calculate_time_format(d_dict):
    corpus = {
        'Study': ['学', '复习', '读', '研', '背'],
        'Coding': ['工作', '制作', 'coding'],
        'Fitness': ['锻炼', '羽毛球'],
        'Eat': ['饭', '菜'],
        'Sleep': ['休'],
        'Entertainment': ['娱乐'],
        'Walk': ['路', '走'],
        'Others': [], # 零碎的事情
        'Blank': [], # 一天中未记录时间
    }
    formated_str = ''
    amount = 0
    for k, v in d_dict.items():
        amount += v
        formated_str += '%s(%0.1f) ' % (k, v/60,)
    return '%sBlank(%0.1f)' % (formated_str, 0 if 24*60-amount < 0 else (24*60-amount)/60, )
