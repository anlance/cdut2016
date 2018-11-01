import requests


# 从每日api获取json格式的数据
from flask import flash


def get_today():
    url = 'http://open.iciba.com/dsSSapi'
    response_obj = requests.get(url=url)
    if response_obj.status_code != 200:
        flash('每日英语官方api已发生变化，请管理员更改', 'warning')
        data = dict({"sid":"3167","tts":"http:\/\/news.iciba.com\/admin\/tts\/2018-10-24-day.mp3","content":"But every once in a while you find someone who's iridescent, and when you do, nothing will compare.","note":"\u4e16\u4eba\u4e07\u5343\u79cd\uff0c\u6d6e\u4e91\u83ab\u53bb\u6c42\uff0c\u65af\u4eba\u5982\u5f69\u8679\uff0c\u9047\u4e0a\u65b9\u77e5\u6709\u3002","love":"1506","translation":"\u5c0f\u7f16\u7684\u8bdd\uff1a\u8fd9\u53e5\u8bdd\u662f\u300a\u6026\u7136\u5fc3\u52a8\u300b\u91cc\u4e00\u53e5\u7ecf\u5178\u7684\u53f0\u8bcd\u3002\u6709\u4eba\u4f4f\u9ad8\u697c\uff0c\u6709\u4eba\u5728\u6df1\u6c9f\uff0c\u6709\u4eba\u5149\u4e07\u4e08\uff0c\u6709\u4eba\u4e00\u8eab\u9508\uff0c\u4e16\u4eba\u4e07\u5343\u79cd\uff0c\u6d6e\u4e91\u83ab\u53bb\u6c42\uff0c\u65af\u4eba\u82e5\u5f69\u8679\uff0c\u9047\u4e0a\u65b9\u77e5\u6709\u3002\u4eba\u751f\u4e2d\u4f1a\u9047\u5230\u5f88\u591a\u4eba\uff0c\u6cdb\u6cdb\u4e4b\u4ea4\u4e0d\u5fc5\u53bb\u5728\u610f\uff0c\u547d\u4e2d\u6ce8\u5b9a\u7684\u90a3\u4e2a\u4eba\u9047\u5230\u4e86\u624d\u77e5\u9053\u4ed6\u662f\u5b58\u5728\u7684\u3002","picture":"http:\/\/cdn.iciba.com\/news\/word\/20181024.jpg","picture2":"http:\/\/cdn.iciba.com\/news\/word\/big_20181024b.jpg","caption":"\u8bcd\u9738\u6bcf\u65e5\u4e00\u53e5","dateline":"2018-04-04","s_pv":"0","sp_pv":"0","tags":[{"id":'s',"name":'s'}],"fenxiang_img":"http:\/\/cdn.iciba.com\/web\/news\/longweibo\/imag\/2018-10-24.jpg"})
        return data
    # response_obj.encoding = 'unicode_escape'
    data = response_obj.json()
    return data
