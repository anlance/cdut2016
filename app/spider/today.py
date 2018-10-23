import requests


# 从每日api获取json格式的数据
def get_today():
    url = 'http://open.iciba.com/dsapi/'
    response_obj = requests.get(url=url)
    # response_obj.encoding = 'unicode_escape'
    data = response_obj.json()
    print(data)
    return data
