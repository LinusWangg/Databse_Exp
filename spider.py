import os
import csv
import random
from re import I
import requests
from lxml import etree
from selenium import webdriver
import time
import psycopg2
conn = psycopg2.connect(database="postgres",user="dboper",password="abcd@123",
                        host="123.60.69.255",port="26000")
cur = conn.cursor()

def randomUserAgent():
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]

    return random.choice(USER_AGENTS)


def getResponse(url, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {
            'User-Agent': randomUserAgent(),
        }

    r = requests.get(url, **kwargs)
    dom = etree.HTML(r.text)

    return dom


def getUserUids(start_users):
    # 保存本次爬取的用户
    next_users = []

    # 爬取 start_users里每个用户的所有关注对象的 uid
    for user in start_users:
        uid = user['uid']
        follow_num = user['follow_num']
        max_page = int(follow_num / PER_NUM) if (follow_num % PER_NUM) == 0 else int(follow_num / PER_NUM)+1
        following_urls = ['https://www.jianshu.com/users/{}/following?page={}'.format(uid, i) for i in
                          range(1, max_page+1)]

        for following_url in following_urls:
            dom = getResponse(following_url)
            items = dom.xpath('//ul/li//div[@class="info"]')

            for item in items:
                user = {}
                try:
                    user['uid'] = item.xpath('./a/@href')[0].split('/')[2]
                    user['follow_num'] = int(item.xpath('./div/span[1]/text()')[0].replace('关注', '').strip())
                    user['fans_num'] = int(item.xpath('./div/span[2]/text()')[0].replace('粉丝', '').strip())
                    user['article_num'] = int(item.xpath('./div/span[3]/text()')[0].replace('文章', '').strip())
                    next_users.append(user)
                    yield user
                except ValueError:
                    pass

    # 递归 将本次的爬取结果作为参数再传递给 getUserUids()
    next_user_uids = getUserUids(next_users)
    # 实现无限爬取
    for user in next_user_uids:
        yield user


def getArt(title_link,fl):
    url = "https://www.jianshu.com"+title_link
    driver = webdriver.Chrome("G:\chromedriver.exe")
    driver.get(url)

    art_content = ""
    div = driver.find_elements_by_xpath("//article/p")
    if(len(div)==0):
        return
    for d in div:
        art_content += d.text+'\n'
    art_time = driver.find_elements_by_xpath("//time")[0].text
    art_author = driver.find_elements_by_xpath("//a[@class='_1OhGeD']")[0].text
    art_title = driver.find_elements_by_xpath("//h1[@class='_1RuRku']")[0].text
    types = [2,1,28,3,17,41,16]
    art_type = random.choice(types)
    try:
        art_pic = driver.find_elements_by_xpath("//article//img")[0].get_attribute('data-original-src')
    except Exception as e:
        art_pic = ""
    sql = "insert into article_article (art_title,art_content,art_author,art_time,art_type,art_pic) values ('{0}','{1}','{2}','{3}',{4},'{5}')".format(
        art_title,art_content,art_author,art_time,art_type,art_pic
    )
    try:
        cur.execute(sql)
    except Exception as e:
        pass
    conn.commit()
    if(fl==0):
        print("change")
        sql = "insert into user_user (user_act,user_name,user_pwd,user_birth) values ('{0}','{1}','{2}','{3}')".format(
            art_author,art_author,"af340ac84b8c78dd5a3f2a89c0a206e1","2021-05-25 00:00:00"
        )
        try:
            cur.execute(sql)
        except Exception as e:
            pass
    conn.commit()
    driver.close()


def getArticleInfo(user):
    uid = user['uid']
    article_num = user['article_num']
    #这里 PER_NUM为 9
    max_page = int(article_num / PER_NUM) if (article_num % PER_NUM) == 0 else int(article_num / PER_NUM)+1
    article_urls = ['https://www.jianshu.com/u/{}?order_by=shared_at&page={}'.format(uid, i) for i in
                    range(1, max_page+1)]
    fl = 0

    for article_url in article_urls:
        dom = getResponse(article_url)
        items = dom.xpath('//ul[@class="note-list"]/li')
        for item in items:
            # 对每个 li标签再提取
            title_link = item.xpath('./div/a/@href')
            for title in title_link:
                getArt(title,fl)
                fl = 1


PER_NUM = 9
seen = []

start_users = [{'uid': '2d260506cb6c', 'follow_num': 308, 'fans_num': 983, 'article_num': 788}]
users = getUserUids(start_users)

for user in users:
    if user['uid'] not in seen:
        seen.append(user['uid'])
        info = getArticleInfo(user)

conn.close()