import re
import requests
from app.spider.spider_utils import get_int_from_str

ua = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {
    'User-Agent': ua
}


# 得到目前已有的所有news
def init_news():
    url = 'http://www.aao.cdut.edu.cn/index/jwtz_gg.htm'
    response_obj = requests.post(url=url, headers=headers)
    response_obj.encoding = 'utf-8'

    # 得到news数目
    number_patter = '<div class="edu-pagination">.*?<span class="p_t">(.*?)</span>.*?<span class="p_t">(.*?)</span>'
    number_obj = re.compile(number_patter, re.S)
    number = number_obj.findall(response_obj.text)
    all_count = get_int_from_str(number[0][0])
    all_page = get_int_from_str(number[0][1])
    url_head = 'http://www.aao.cdut.edu.cn/index/jwtz_gg/'
    news = []

    for i in range(all_page-1):
        real_num = i + 1
        url_tail = str(real_num) + '.htm'
        page_url = url_head + url_tail
        # 获取其他页的news
        cur_news, sum = get_onepage(page_url)
        for item in cur_news:
            if item not in news:
                news.append(item)

    # 获取首页的news
    cur_news, sum = get_onepage(url=url)
    # 去掉首页和第二页的重复news
    cur_news_num = all_count - len(news)
    for i in range(cur_news_num):
        news.append(cur_news[i])
    print(len(news))
    return news, all_count


# 更新news
def update_news(total):
    url = 'http://www.aao.cdut.edu.cn/index/jwtz_gg.htm'
    news = []
    cur_news, sum = get_onepage(url=url)
    if sum > total:
        news_num_update = sum - total
        print('--------')
        for i in range(news_num_update):
            news.append(cur_news[i])
        print(sum)
        print(total)
    return news


# 得到一页的news
def get_onepage(url):
    response_obj = requests.post(url=url, headers=headers)
    response_obj.encoding = 'utf-8'

    # 获取news
    news_div_patter = '<div class="content">(.*?)</div>'
    new_div_obj = re.compile(news_div_patter, re.S)
    news_div = new_div_obj.findall(response_obj.text)

    news_patter = '<li>.*?<a href="(.*?)".*?<span>(.*?)</span>.*?<span.*?>(.*?)</span>'
    news_obj = re.compile(news_patter, re.S)
    news = news_obj.findall(news_div[0])

    # 得到news数目
    number_patter = '<div class="edu-pagination">.*?<span.*?>(.*?)</span>'
    number_obj = re.compile(number_patter, re.S)
    number = number_obj.findall(response_obj.text)
    sum = get_int_from_str(number[0])

    return news, sum



