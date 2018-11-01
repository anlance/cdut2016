import urllib.request
import urllib.parse
import time
import hashlib
from http import cookiejar
import re


def login_cdut(username, pwd):
    login_url = 'http://202.115.133.173:805/Common/Handler/UserLogin.ashx'
    hash_pwd = hashlib.md5(pwd.encode()).hexdigest()
    sign = int(round(time.time()*1000))
    signed_pwd = hashlib.md5((username+str(sign)+hash_pwd).encode()).hexdigest()
    data = {
        'Action': 'Login',
        'userName': username,
        'pwd': signed_pwd,
        'sign': sign
    }
    login_data = urllib.parse.urlencode(data).encode()
    cookie = cookiejar.CookieJar()
    cookie_hand = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookie_hand)
    request_obj = urllib.request.Request(url=login_url, data=login_data)
    response = opener.open(request_obj)

    target_url = 'http://202.115.133.173:805/SearchInfo/Score/ScoreList.aspx'
    request_obj = urllib.request.Request(target_url)
    try:
        response = opener.open(request_obj)
    except:
        return response, 404
    response_obj = response.read().decode()
    return response_obj, response.status


def parse_stu_score(response_obj, status):
    if status != 200:
        return []
    patter = '<li class="item">.*?style="width: 6%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 20%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 7%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 4%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 4%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 10%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 10%;">.*?\s+(.*?)&nbsp.*?</div>' \
             '.*?style="width: 15%;">.*?\s+(.*?)&nbsp.*?</div>'
    re_obj = re.compile(patter, re.S)
    match_list = re_obj.findall(response_obj)
    return match_list

