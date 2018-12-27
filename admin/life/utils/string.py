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
