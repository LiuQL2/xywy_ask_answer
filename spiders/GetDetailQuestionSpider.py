# /usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
import json
from spiders.BaseSpider import BaseSpider


# http://club.xywy.com/static/20171007/129666667.htm

class DetailQuestionSpider(BaseSpider):
    def __init__(self,url,use_proxy=False):
        self.url = url
        self.selector = self.process_url_request(url=url,xpath_type=True,whether_decode=True,encode_type='GBK',
                                                 use_proxy=use_proxy)

    def parse(self,question):
        """
        解析网页，获取每一个问题的具体内容
        :param question: dict，包含问题的标题、内容、提问日期、所属疾病
        :return: 包含详细信息的question
        """
        try:
            question["post_time"] = self.selector.xpath('//div[@class="f12 graydeep Userinfo clearfix pl29"]/span[7]/text()')[0]
            question["user_info"] = self.__get_user_info()
            question["answer"] = self.__get_answer()
            return question
        except Exception, e:
            print traceback.format_exc(), e.message
            return None

    def __get_user_info(self):
        """
        获取提问的用户信息，这里只保留用户id
        :return: dict，包含用户id
        """
        user = {}
        user["user_id"] = self.selector.xpath('//div[@class="f12 graydeep Userinfo clearfix pl29"]/span[1]/text()')[0]
        try:
            user["user_gender"] = self.selector.xpath('//div[@class="f12 graydeep Userinfo clearfix pl29"]/span[3]/text()')[0]
            user["user_gender"] = user["user_gender"].replace("\t","")
        except:
            user["user_gender"] = None
        try:
            user["user_age"] = self.selector.xpath('//div[@class="f12 graydeep Userinfo clearfix pl29"]/span[5]/text()')[0]
        except:
            user["user_age"] = None
        return user

    def __get_answer(self):
        """
        获得问题的医生回答
        :return: list，每一个元素是一个dict，包含了回答各种信息：回答的医生url、回答内容、回答时间
        """
        answer_list = self.selector.xpath('//div[@class="docall clearfix "]')
        temp_answer_list = []
        for answer in answer_list:
            temp_answer = {}
            temp_answer["doctor_url"] = answer.xpath('div[@class="zyhftop pl29 pt20 clearfix pr"]/div[1]/div[2]/div[1]/div[1]/a/@href')[0]
            answer = answer.xpath('div[@class="pt10 mb5 clearfix pr qsdetail"]')[0]
            temp_answer["reply_time"] = answer.xpath('div[2]/p[1]/span/text()')[0]
            body_content = answer.xpath('div[2]/div[1]')[0]
            temp_answer["answer_body"] = body_content.xpath('string(.)')
            # 获得追问的详细内容，如果为空则没有该字段
            ask_again_list = self.__get_ask_again(answer=answer)
            if ask_again_list is None:
                pass
            else:
                temp_answer["ask_again"] = ask_again_list
            temp_answer_list.append(temp_answer)
        return temp_answer_list

    def __get_ask_again(self, answer):
        """
        获得追问的详细内容
        :param answer: 包含一个answer的selector，可以使用xpath
        :return: list，每一个元素是一个追问信息：追问患者、追问内容、追问时间，如果是针对追问的回答则为：回答医生url、回答内容、回答时间
        """
        ask_again = answer.xpath('div[2]/div[@class="appdoc appxian ml20 mr20 mt15 pb10 clearfix f14"]')
        if len(ask_again) == 0:
            return None
        else:
            ask_again_list = ask_again[0].xpath('div')
            temp_ask_again_list = []
            temp_ask_again = {}
            for ask_again in ask_again_list:
                if len(ask_again.xpath('div/p/span')) == 2:
                    temp_ask_again['user_id'] = ask_again.xpath('div/p/span[1]/text()')[0]
                    temp_ask_again['ask_time'] = ask_again.xpath('p/span/text()')[0]
                else:
                    temp_ask_again['doctor_url'] = ask_again.xpath('div/p/a/@href')[0]
                    temp_ask_again['reply_time'] = ask_again.xpath('p/span/text()')[0]
                ask_again_content = ask_again.xpath('div/div')[0]
                temp_ask_again['body'] = ask_again_content.xpath('string(.)')
                temp_ask_again_list.append(temp_ask_again)
            return temp_ask_again_list



if __name__ == "__main__":
    url = "http://club.xywy.com/static/20171007/129665425.htm"
    spider = DetailQuestionSpider(url = url)
    question = spider.parse(question={})
    print json.dumps(question)