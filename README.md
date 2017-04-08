# xywy_ask_answer
Distributed crawler for www.club.xywy.com.
# 爬虫说明
该爬虫在RabbitMQ的架构之上，实现多台机器之前的通信，进而实现分布式爬虫。
## configuration
配置该爬虫的相关信息，以及一些访问设置，包括访问速度、代理服务器、RabbitMQ中保存数据的队列名称等。
## consumer
