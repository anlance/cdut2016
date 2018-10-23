import requests


# 从每日api获取json格式的数据
from flask import flash


def get_today():
    url = 'http://open.iciba.com/dsapi'
    response_obj = requests.get(url=url)
    if response_obj.status_code != 200:
        flash('每日英语官方api已发生变化，请管理员更改', 'warning')
        data = dict(sid="3166", tts="http:\/\/news.iciba.com\/admin\/tts\/2018-10-23-day.mp3",
                            content="Everyone you see exists together in a delicate balance.",
                            note="\u4e16\u754c\u4e0a\u6240\u6709\u7684\u751f\u547d\u90fd\u5728\u5fae\u5999\u7684\u5e73\u8861\u4e2d\u751f\u5b58\u3002",
                            love="321",
                            translation="\u5c0f\u7f16\u7684\u8bdd\uff1a\u6211\u4eec\u6765\u5230\u8fd9\u4e2a\u4e16\u754c\uff0c\u7728\u7740\u773c\u8d70\u8fdb\u9633\u5149\u3002\u60f3\u770b\u7684\uff0c\u6c38\u8fdc\u770b\u4e0d\u591f\uff1b\u60f3\u505a\u7684\uff0c\u6c38\u8fdc\u505a\u4e0d\u5b8c\uff1b\u60f3\u5bfb\u627e\u7684\uff0c\u6c38\u8fdc\u6ca1\u6709\u5c3d\u5934\u3002\u65e5\u51fa\u65e5\u843d\uff0c\u7a7f\u8fc7\u84dd\u5929\uff0c\u5728\u4f1f\u5927\u4e0e\u6e3a\u5c0f\u4e2d\u627e\u5230\u81ea\u5df1\u7684\u5e73\u8861\uff0c\u8fd9\u5c31\u662f\u751f\u547d\u7684\u8f6e\u56de\u3002\r\n",
                            picture="http:\/\/cdn.iciba.com\/news\/word\/20181023.jpg",
                            picture2="http:\/\/cdn.iciba.com\/news\/word\/big_20181023b.jpg",
                            caption="\u8bcd\u9738\u6bcf\u65e5\u4e00\u53e5", dateline="2036-12-12", s_pv="0", sp_pv="0",
                            fenxiang_img="http:\/\/cdn.iciba.com\/web\/news\/longweibo\/imag\/2018-10-23.jpg")
        return data
    # response_obj.encoding = 'unicode_escape'
    data = response_obj.json()
    return data
