#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
用来抓取病例和心得里面帖子URL的类，该类首先将帖子的URL保存在一个csv文件中。
对于URL保存的文件，在开始的时候如果存在的话，需要删除。
"""

# Author: Liu Qianlong  <LiuQL2@163.com>
# Date: 2016.11.06

import random
import socket
import sys
import os
import urllib.request
from urllib.error import URLError
import traceback

import lxml.etree
sys.path.append(os.getcwd().replace("spiders",""))

from configuration.settings import USER_AGENTS as user_agents
from database.IOHandler import FileIO
from configuration.settings import PROXIES as proxies


class BaseSpider(object):
    """
    基础的爬虫类，实现user_agent的随机选取，从url到request再到需要的网页数据类型，可以转化成使用xpath提取的类型，也可以
    以string的类型获得网页源码。
    """
    # def __init__(self, *args, **kwargs):
    #     pass

    def get_header(self):
        """
        获得头文件。
        :return:返回一个header。
        """
        return {'User-Agent':random.choice(user_agents)}

    def set_proxy(self):
        proxy_temp = {'http': random.choice(proxies)}
        proxy_handler = urllib.request.ProxyHandler(proxy_temp)
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener=opener)
        print('*********',proxy_temp)

    def process_url_request(self,url,try_number=20, timeout=100,xpath_type=True, whether_decode=False, encode_type='utf-8',use_proxy=False):
        """
        从一个url，返回该url对应的网页内容，根据需求不同，返回不同数据类型的网页数据。
        :param url: 目标url
        :param try_number: 尝试的次数
        :param timeout: 超时时间。
        :param xpath_type: 是否转化成可以使用xpath的数据类型。
        :param whether_decode: 是否需要转换编码。
        :param encode_type: 如果需要转换编码，则编码格式是什么。
        :param use_proxy: 是否使用代理服务器，boolean
        :return: 返回对应的数据，多次尝试失败后返回None.
        """
        doc = None
        try_index = 0
        if xpath_type == True:
            while doc == None:
                if use_proxy == True:
                    self.set_proxy()
                else:
                    pass
                request = urllib.request.Request(url=url, headers=self.get_header())
                doc = self.__process_request_xpath__(request=request,timeout=timeout,whether_decode=whether_decode, encode_type=encode_type)
                try_index = try_index + 1
                if try_index > try_number:
                    break
                else:
                    pass
            return doc
        else:
            while doc == None:
                request = urllib.request.Request(url=url, headers=self.get_header())
                doc = self.__process_request__(request=request,timeout=timeout)
                try_index = try_index + 1
                if try_index > try_number:
                    break
                else:
                    pass
            return doc

    def __process_request_xpath__(self,request,timeout=100, whether_decode=False,encode_type='utf-8'):
        """
        处理request请求，返回一个可以使用xpath语法的数据类型。
        :param request: 需要处理的request。
        :param timeout:超时时间
        :param whether_decode: 是否需要转换编码
        :return:返回一个可以用xpath解析的selector格式。
        """
        try:
            response = urllib.request.urlopen(request,timeout=timeout)
            try:
                doc = response.read()
                response.close()
                if whether_decode == True:
                    doc = doc.decode(encode_type, 'ignore')
                else:
                    pass
                doc = lxml.etree.HTML(doc)
            except Exception as e:
                FileIO.exceptionHandler(message=e.args[0])
                print(traceback.format_exc(), e.args[0])
                doc = None
            return doc
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to raach a server.')
                print('Reaseon: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server could not fulfill the request.')
                print('Error code: ', e.code)
                print('Reason: ', e.reason)
            FileIO.exceptionHandler(message= e.reason)
            print(traceback.format_exc(), e.reason)
            return None
        except socket.timeout as e:
            print('Error code: socket timeout', e)
            FileIO.exceptionHandler(message= e.args[0])
            print(traceback.format_exc(), e.args[0])
            return None
        except Exception as e:
            FileIO.exceptionHandler(message=e.args[0])
            print(traceback.format_exc(), e.args[0])
            print('Do Not know what is wrong.')
            return None

    def __process_request__(self,request,timeout = 100):
        """
        处理request请求，以string的类型返回网页内容。
        :param request:request的请求
        :param timeout:超时时间
        :return:返回内容，失败返回None
        """
        try:
            response = urllib.request.urlopen(request, timeout=timeout)
            doc = response.read()
            return doc
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to raach a server.')
                print('Reaseon: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server could not fulfill the request.')
                print('Error code: ', e.code)
                print('Reason: ', e.reason)
            FileIO.exceptionHandler(message= e.reason)
            print(traceback.format_exc(), e.reason)
            return None
        except socket.timeout as e:
            print('Error code: socket timeout', e)
            FileIO.exceptionHandler(message=e.args[0])
            print(traceback.format_exc(), e.args[0])
            return None
        except Exception as e:
            FileIO.exceptionHandler(message=e.args[0])
            print(traceback.format_exc(), e.args[0])
            print('Do Not know what is wrong.')
            return None