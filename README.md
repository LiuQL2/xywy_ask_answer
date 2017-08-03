# xywy_ask_answer
Distributed crawler for www.club.xywy.com.
# 1.爬虫说明
该爬虫在RabbitMQ的架构之上，实现多台机器之前的通信，进而实现分布式爬虫。
## (1) configuration
配置该爬虫的相关信息，以及一些访问设置，包括访问速度、代理服务器、RabbitMQ中保存数据的队列名称等。
## (2) consumer
里面包含三个consumer.
day_url_consumer,用来处理每一天的url连接，并获得该日期下所有页面的url，同时调用ProcessDayUrl.ProcessDayUrl爬虫将结果保存到RabbitMQ.
page_url_consumer,用来处理每一个页面的url，每一个页面包含20条问题信息，获得问题信息后调用ProcessDayUrl.GetOnePageQuestion爬虫，将问题信息保存到RabbitMQ.
question_consumer,用来将RabbitMQ中的问题信息数据保存到本地文件.
## (3) database
一些数据传输的工具
IOHandler:处理文件的读写.
MysqlDatabaseClass：处理mysql数据库的读写.
RabbitMQ:对RabbitMQ服务器进行操作.
SqliteDatabaseClass:对sqlite数据库进行操作.
## (4) logs
保存日志文件，主要是错误信息.
## （5） producer
day_url_producer:用来产生每一天的页面连接，保存到RabbitMQ服务器中.
## （6） result
保存数据的目录.
## （7） spiders
爬虫文件.
BaseSpider:基础的爬虫，实现对网站的访问等功能.
GetDayUrlSpider:获取每一天url的爬虫.
ProcessDayUrlSpider:处理每一天的url，包括两部分：a.从一天url中获取这一天所有问题的页面；b.从一个页面中获取该页面下所有的问题信息.

# 2.使用说明
(1)配置好setting.py文件.
(2)启动RabbitMQ服务器.
(3)首先运行day_url_producer,且只运行一次即可,不要重复运行.
(4)运行day_url_producer,可以运行多个，可结束重新运行.
(5)运行page_url_consumer,因为page url数量太多，所以这部分工作量最大，建议运行多个改程序.
(6)运行quesiton_consumer,运行一个即可满足需求.

# 3. 分布式部署
......
