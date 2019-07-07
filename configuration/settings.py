# -*- coding:utf-8 -*-

# 项目的参数配置，包括数据库表（表名、属性名、主键）、维护人员邮箱、需要访问的网站首页以及被封的状态；
# 如果没有参数没有，比如没有数据库
import pika

"""
以下配置爬虫服务器信息，主要是RabbitMQ。
"""
# 数据库信息配置，这里用于连接数据库，各个属性是否必需如下
DATABASE_INFO = dict(
    host='localhost',#数据库所在主机，必需
    user='qianlong',#用户名，必需
    passwd='962182',#用户密码，必需
    database='xywy_fudan',#数据库名称，必需
    port=3306,#端口号，必需
    charset='utf8',#数据库编码方式，必需
    use_unicode = True,
)

MongoDB_INFO= dict(
    host = 'localhost',
    port = 27017
)


#配置运行rabbitmq的主机服务器信息
RABBITMQ_CONNECTION_PARA = pika.ConnectionParameters(
    host='ip of your RabbitMQ server',
    port=5672,
    credentials=pika.PlainCredentials(username='username',password='password'),
    heartbeat=0
)

#设置每一个url尝试的次数，url_try_number,当超过这个次数后，即使url访问失败，也不再返回到rabbit中
URL_TRY_NUMBER = 10


"""
以下部分为抓取问题的简要信息而设置，包括网站上有多少问题页面、抓取问题的年份、以及保存数据的文件名、RabbitMQ里面的一些设置等。
"""
#设置在http://club.xywy.com/keshi/1.html页面，每天问题连接页面，共有多少页。
PAGE_NUMBER = 68
#设置想抓取哪一年的数据，如果为None，表示抓取所有年份的数据，否则写出年份
DATA_YEAR = '2017' #表示抓取2017年的数据
# DATA_YEAR = None #表示抓取全部年份的数据

#保存最终问题的文件名称,文件将保存到本项目下result文件夹中。每次都是追加内容，不会删除之前的数据，运行爬虫需要注意
QUESTION_SAVE_FILE = '2017_question.json'

#每次访问网站后暂停时间
TIME_SLEEP = 3

#用来存储2017年中每一天的queue和exchange信息。http://club.xywy.com/keshi/2017-11-16/1.html
DAY_URL_QUEUE_EXCHANGE = dict(
    exchange='2017_day_url_exchange',
    routing_key = '2017_day_url_routing_key',
    queue = '2017_day_url_queue',
    exchange_type='direct',
    queue_durable=True,
)

#用来存储每一个页面url的queue和exchange，页面如：http://club.xywy.com/keshi/2017-11-16/3.html
PAGE_URL_QUEUE_EXCHANGE = dict(
    exchange='2017_page_url_exchange',
    routing_key='2017_page_url_routing_key',
    queue='2017_page_url_queue',
    exchange_type='direct',
    queue_durable=True,
)

#用来保存问题的queue和exchange信息。
QUESTION_QUEUE_EXCHANGE = dict(
    exchange='2017_question_exchange',
    routing_key='2017_question_routing_key',
    queue='2017_question_queue',
    exchange_type='direct',
    queue_durable=True,
)

DISEASE_URL_QUEUE_EXCHANGE = dict(
    exchange = 'disease_url_exchange',
    routing_key = 'disease_url_routing_key',
    queue = 'disease_url_queue',
    exchange_type = 'direct',
    queue_durable = True,
)


"""
为抓取问题详细信息而设置。详细信息包含每个问题的医生回答（回答的医生、回答的时间、回答的内容）
"""
# 确定需要抓取详细信息的疾病URL，其实是网站上的二级科室连接。下面的每一个网址实际上是一种疾病，将疾病对应的二阶科室连接加入到里面，那么在获
# 取详细问题url时，对应该疾病的url就会被抓取数据。
DETAIL_DISEASE_URL = [
    "http://club.xywy.com/small_346.htm"
]

#对应的年份文件夹，保存了简要信息的数据
# DETAIL_YEAR_DIR="/Users/qianlong/Desktop/"
DETAIL_YEAR_DIR="/Volumes/LiuQL/fudan_sds/xywy_ask/2015/"
DETAIL_QUESTION_SAVE_FILE="2015_detail_question.json"

#queue和exchange信息，用来保存需要详细信息的问题URL。
DETAIL_QUESTION_URL_QUEUE_EXCHANGE = dict(
    exchange='2015_detail_question_url_exchange',
    routing_key='2015_detail_question_url_routing_key',
    queue='2015_detail_question_url_queue',
    exchange_type='direct',
    queue_durable=True,
)

#queue和exchange信息，用来保存需要详细信息的问题URL。
DETAIL_QUESTION_QUEUE_EXCHANGE = dict(
    exchange='2015_detail_question_exchange',
    routing_key='2015_detail_question_routing_key',
    queue='2015_detail_question_queue',
    exchange_type='direct',
    queue_durable=True,
)





"""
代理设置。
"""
#是否使用代理服务器
USE_PROXY = False
#配置ip代理服务器
PROXIES = [
    "http://username:password@yourip1:port",
    "http://username:password@yourip2:port"
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

