# /usr/bin/env python
# -*- coding:utf-8 -*-
"""
获取每个问题的详细信息，这里包含针对问题的回复医生、回复时间、回复内容等，一个具体的例子如下：

{
  "question_url": "http://club.xywy.com/static/20161231/124514524.htm",
  "post_time": "2016-12-31 21:38:45",
  "question_title": "这该怎么治？有什么办法？",
  "disease": "肿瘤科",
  "question_body": "胆管癌晚期。有疼感。吃不进去食，有时候会呕吐，干呕，尿少，该怎么治疗，有什么办法？",
  "user_info": {
    "user_id": "会员113108581"
  },
  "disease_url": "http://club.xywy.com/small_346.htm",
  "answer": [
    {
      "reply_time": "2016-12-31 21:46:56",
      "doctor_url": "http://z.xywy.com/doc/zhangkaiys1297/",
      "answer_body": "主要就是保持胆汁排出通畅是关键，然后就是对症治疗，以减轻患者痛苦提高生活质量为主要"
    },
    {
      "reply_time": "2016-12-31 22:11:44",
      "doctor_url": "http://club.xywy.com/doc_card/36450269",
      "answer_body": "问题分析：你好，胆管癌晚期最好采用有效的传统中药保守治疗，中医中药长期临床实践积累了许多非常有效的治疗方法。意见建议：胆管癌晚期建议你采用传统中药虫草、猪苓、明党参、桑寄生、青阳参、香菇、红豆蔻、桑白皮、杜仲、降香、茯苓、白术、八月札、知母、片姜黄、制南星、山萸肉、木瓜、仙茅、制半夏、射干、当归、土鳖虫、青黛、肉桂、苦参、金精粉、葫芦巴、白癣皮、赤芍、山豆根、远志、泽泻、金银花、乌术粉、制鳖甲、连翘、紫草、桃仁、三七等配合治疗。希望你正确治疗，早日康复！"
    },
    {
      "reply_time": "2017-01-01 09:44:42",
      "doctor_url": "http://club.xywy.com/doc_card/75756414",
      "answer_body": "问题分析：您好，胆管癌晚期患者常表现出黄疸、腹痛腹胀、恶心呕吐、消瘦、皮肤瘙痒、大便习性改变等症状，晚期肿瘤细胞大多已经转移，多数患者已经失去手术机会，建议接受中医中药整体治疗抑制癌肿发展增强体质提升患者免疫能力，缓解呕吐疼痛症状降低肿瘤对人体的消耗减轻痛苦改善患者生活质量延长生命。意见建议：胆管癌多因肝郁气滞、饮食不节、湿热壅阻、日久化火蕴蒸于内、痹阻不通而形成的，中医治疗通过严格辨证后，运用健脾益气、补养气血、解毒散结等中药，调节机体阴阳气血平衡恢复五脏六腑功能改善患者全身身体状况最大程度的延长患者生存期。z"
    }
  ]
}

"""

import traceback
import json
from spiders.BaseSpider import BaseSpider


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