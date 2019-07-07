# xywy_ask_answer
Distributed crawler for http://club.xywy.com/small_346.htm.
Entry page:http://club.xywy.com/keshi/2.html
# 1.爬虫说明
该爬虫在RabbitMQ的架构之上，实现多台机器之前的通信，进而实现分布式爬虫。
### 1. configuration
配置该爬虫的相关信息，以及一些访问设置，包括访问速度、代理服务器、RabbitMQ中保存数据的队列名称等。
### 2. consumer
里面包含三个consumer.
 * day_url_consumer,用来处理每一天的url连接，并获得该日期下所有页面的url，同时调用ProcessDayUrl.ProcessDayUrl爬虫将结果保存到RabbitMQ.
 * page_url_consumer,用来处理每一个页面的url，每一个页面包含20条问题信息，获得问题信息后调用ProcessDayUrl.GetOnePageQuestion爬虫，将问题信息保存到RabbitMQ.
 * question_consumer,用来将RabbitMQ中的问题信息数据保存到本地文件.
### 3. database
一些数据传输的工具
 * IOHandler:处理文件的读写.
 * MysqlDatabaseClass：处理mysql数据库的读写.
 * RabbitMQ:对RabbitMQ服务器进行操作.
 * SqliteDatabaseClass:对sqlite数据库进行操作.
### 4. logs
保存日志文件，主要是错误信息.
### 5. producer
day_url_producer:用来产生每一天的页面连接，保存到RabbitMQ服务器中.
### 6. result
保存数据的目录.
### 7. spiders
爬虫文件.
 * BaseSpider:基础的爬虫，实现对网站的访问等功能. 这里是爬虫最基本的功能，也就是能够获取数据的脚本。其他的spider都会继承这个类来实现相应
 的爬虫功能，可以详细看一下这个文件代码.
 * GetDayUrlSpider:获取每一天url的爬虫.
 * ProcessDayUrlSpider:处理每一天的url，包括两部分：a.从一天url中获取这一天所有问题的页面；b.从一个页面中获取该页面下所有的问题信息.

# 2. 使用说明
### 1. 问题基本信息抓取
 * (1) 配置好setting.py文件.
 * (2) 启动RabbitMQ服务器.
 * (3) 首先运行day_url_producer.py,且只运行一次即可,不要重复运行.
 * (4) 运行day_url_consumer.py,可以运行多个，可结束重新运行.
 * (5) 运行page_url_consumer.py,因为page url数量太多，所以这部分工作量最大，建议运行多个改程序.
 * (6) 运行question_consumer.py,运行一个即可满足需求.

### 2. 使用说明-问题详细信息抓取
 * (1) 配置好setting.py文件，即指定详细问题的疾病、问题基本信息文件，以及Rabbit MQ的信息。
 * (2) 运行detail_question_url_producer.py
 * (3) 运行detail_question_url_consumer.py

# 3. 分布式部署
### 1. RabbitMQ的安装与简单学习
* 首先在[官网](https://www.rabbitmq.com/)了解RabbitMQ的架构、基本概念等；
* [参考这里](https://www.rabbitmq.com/download.html)进行安装；
* [参考这里](https://www.rabbitmq.com/getstarted.html)学习RabbitMQ的简单入门；
* [参考这里](https://www.jianshu.com/p/7d071bffea24)添加用户、密码、角色、权限等。

### 2. 部署
* 首先启动RabbitMQ服务器，并在configuration/settings.py中进行配置服务器IP、用户名、密码；
* 在configuration/settings.py中配置RabbitMQ消息队列等其他参数；
* 爬虫代码在在不同的机器上都复制一份，保证settings.py中RabbitMQ的配置一样，然后可以在不同的机器上可以运行相应的脚本，这样各个机器抓取的数
就可以在传到RabbitMQ 服务器上；

# 4. 代理服务器
* 配置VPN，假设购买的有云服务器，那么可以通过安装[Squid](http://www.squid-cache.org/)进行服务器代理，
通过[httpd-tools](https://httpd.apache.org/)配合Squid实现用户认证的VPN。[这里](https://www.server-world.info/en/note?os=CentOS_7&p=squid&f=1)
以在CentOS 7上安装为例，可以在此网站上选择其他操作系统进行配置。
* 在configuration/settings.py中设置USE_PROXY = True，并按照给出的格式添加上面配置的VNP用户名、密码、IP、端口；
