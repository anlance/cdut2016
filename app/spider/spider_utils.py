import re


# 获取字符串中的第一串数字
def get_int_from_str(string):
    num = re.findall(r'\D*(\d*)\D*', string=string)
    return int(num[0])

