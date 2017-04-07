# -*- coding:utf-8 -*-

# 项目的参数配置，包括数据库表（表名、属性名、主键）、维护人员邮箱、需要访问的网站首页以及被封的状态；
# 如果没有参数没有，比如没有数据库


# 数据库信息配置，这里用于连接数据库，各个属性是否必需如下
DATABASE_INFO = dict(
    host='localhost',#数据库所在主机，必需
    user='qianlong',#用户名，必需
    passwd='962182',#用户密码，必需
    database='xywy_communication',#数据库名称，必需
    port=3306,#端口号，必需
    charset='utf8',#数据库编码方式，必需
    use_unicode = True,
)


#配置运行rabbitmq的主机服务器信息
MASTER_INFO = dict(
    host='127.0.0.1',
    port=5672,
    user='longer',
    password='longer'
)


#设置在www.club.xywy.com页面，每天问题连接页面，共有多少页。
PAGE_NUMBER = 58
#设置想抓取哪一年的数据，如果为None，表示抓取所有年份的数据，否则写出年份
DATA_YEAR = '2016' #表示抓取2016年的数据
# DATA_YEAR = None #表示抓取全部年份的数据

#用来存储2016年中每一天的queue和exchange信息。http://club.xywy.com/keshi/2016-11-16/1.html
DAY_URL_QUEUE_EXCHANGE = dict(
    exchange='2016_day_url_exchange',
    routing_key = '2016_day_url_routing_key',
    queue = '2016_day_url_queue',
    exchange_type='direct',
    queue_durable=False,
)

#用来存储每一个页面url的queue和exchange，页面如：http://club.xywy.com/keshi/2016-11-16/3.html
PAGE_URL_QUEUE_EXCHANGE = dict(
    exchange='2016_page_url_exchange',
    routing_key='2016_page_url_routing_key',
    queue='2016_page_url_queue',
    exchange_type='direct',
    queue_durable=False,
)

#用来保存问题的queue和exchange信息。
QUESTION_URL_QUEUE_EXCHANGE = dict(
    exchange='2016_question_exchange',
    routing_key='2016_question_routing_key',
    queue='2016_question_queue',
    exchange_type='direct',
    queue_durable=False,
)



#是否使用代理服务器
USE_PROXY = True
#配置ip代理服务器
PROXIES = [
    "http://longer:longer@104.194.84.47:3128/",
    "http://longer:longer@123.206.7.172:3128/",
    "http://sww1:sww@139.199.30.89:808/",
    # "http://139.199.33.179:808/",
    "http://sww:sww@123.206.125.155:808/",
    "http://sww:sww@119.29.113.89:808/",
]


# User agents
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
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

