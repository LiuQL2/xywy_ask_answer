#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 对数据库进行增删改查的类.
用于对数据库进行增删改查。

'''

# Author: Liu Qianlong <LiuQL2@163.com>
# Date: 2016.10.17

import _mysql_exceptions as ___mysql_exceptions
import MySQLdb
import os
import sys
from configuration.parameters import DATABASE_INFO as database_info
import MySQLdb.cursors
from twisted.enterprise import adbapi
reload(sys)
sys.setdefaultencoding('utf-8')


class MySQLDatabaseClass(object):
    def __init__(self):
        """
        类的初始化
        :return:无返回数据
        """
        try:
            conn = MySQLdb.connect(host=database_info['host'],
                               user=database_info['user'],
                               passwd=database_info['passwd'],
                               db=database_info['database'],
                               port=database_info['port'],
                               charset=database_info['charset'])
            self.__connector = conn
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def select(self, table, record = None, database = None):
        """
        在数据库表中进行查询操作,当record为空的时候是查询该表内的所有数据，否则根据record进行有条件查询，当数据库名称为空时，默认为配置文件中的数据库信息。
        :param table:需要查询的数据库表。
        :param record:根据哪一个属性进行查询，必需是字典的形式，dict,而且字典的key必需与数据库中的表列名对应。
        :param database: 表table所在的数据库，如果为空，默认为parameters文件中配置的数据库。
        :return: 返回查询结果，是一个list，里面的每一个元素是一个字典，字典的key与数据库表中的列名相同。
        """
        try:
            cursor = self.__connector.cursor()
            if database == None:
                database = database_info['database']
            else:
                pass
            if record == None:
                cursor.execute('select * from ' + database + '.' + table)
                data_tuple = cursor.fetchall()
            else:
                sql = 'select * from '+ database + '.' + table +' where '
                values = []
                for (key, value) in record.items():
                    sql = sql + key + ' = %s and '
                    values.append(value)
                if 'and' in sql[len(sql)-4:len(sql)]:
                    sql = sql[0:len(sql)-5]
                else:
                    pass
                cursor.execute(sql, values)
                data_tuple = cursor.fetchall()
            cursor.close()
            return self.__tuple_to_list__(table = table, data_tuple = data_tuple, database=database)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return list()

    def insert(self, table, record, database = None):
        """
        用于数据库表的插入操作，一次插入一个记录。
        :param table:需要插入的表的名称
        :param record:需要插入的数据，必需是一个字典，而且字典的key与数据库表table中列名一一对应。
        :param database: 表table所在的数据库，如果为空，默认为parameters文件中配置的数据库。
        :return:没有返回数据
        """
        try:
            cursor = self.__connector.cursor()
            if database == None:
                database = database_info['database']
            else:
                pass
            sql1 = 'insert into ' + database + '.' + table +' ('
            sql2 = 'values ('
            values = []
            for (key, value) in record.items():
                sql1 = sql1 + key + ','
                sql2 = sql2 + '%s,'
                values.append(value)
            sql1 = sql1[0:len(sql1)-1] + ') '
            sql2 = sql2[0:len(sql2)-1] + ') '
            sql = sql1 + sql2
            cursor.execute(sql, values)
            self.__connector.commit()
            cursor.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def delete(self, table, record,database = None):
        """
        用来删除table表中record数据
        :param table: 需要删除数据的表。
        :param record: 需要在表中删除的数据。必需是一个字典，而且字典的key与table表中的列名一一对应。
        :param database: 表table所在的数据库，如果为空，默认为parameters文件中配置的数据库。
        :return:没有返回数据。
        """
        try:
            cursor = self.__connector.cursor()
            if database == None:
                database = database_info['database']
            else:
                pass
            sql = 'delete from ' + database + '.' + table +' where '
            values = []
            for (key, value) in record.items():
                sql = sql + key + ' = %s and '
                values.append(value)
            sql = sql[0:len(sql)-5]
            cursor.execute(sql, values)
            self.__connector.commit()
            cursor.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def update(self,table, record, primary_key, database = None):
        """
        更新数据库中的数据。
        :param table: 需要更新的数据库表。
        :param record: 新数据，必须是字典，且字典key和数据库table表列名一一对应。
        :param primary_key: 需要更新的记录的主键，必需是一个字典，且字典key和数据库table表列名一一对应。
        :param database: 表table所在的数据库，如果为空，默认为parameters文件中配置的数据库。
        :return: 没有返回数据。
        """
        try:
            cursor = self.__connector.cursor()
            if database == None:
                database = database_info['database']
            else:
                pass
            sql1 = 'update ' + database + '.' + table + ' set '
            sql2 = ' where '
            values = []
            for (key, value) in record.items():
                sql1 = sql1 + key + ' = %s,'
                values.append(value)
            for (key, value) in primary_key.items():
                sql2 = sql2 + key + ' = %s and '
                values.append(value)
            sql1 = sql1[0:len(sql1) - 1]
            sql2 = sql2[0:len(sql2) - 5]
            sql = sql1 + sql2
            print sql
            cursor.execute(sql, values)
            self.__connector.commit()
            cursor.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])

    def close(self):
        """
        关闭数据库的连接。
        :return: 无返回数据。
        """
        self.__connector.close()

    def __get_column_name__(self, table, database = None):
        """
        用于获得表的列名
        :param table:需要获得列名的表名。
        :param database:表table所在的数据库，如果为空，则默认为parameters文件中配置的数据库表。
        :return:返回表table的列名，类型为tuple
        """
        try:
            cursor = self.__connector.cursor()
            if database == None:
                database = database_info['database']
            else:
                pass
            cursor.execute('select column_name from information_schema.columns where table_name = %s and table_schema = %s;',[table, database])
            data_tuple = cursor.fetchall()
            return data_tuple
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return tuple()

    def __tuple_to_list__(self, table,database, data_tuple = tuple()):
        """
        用于将查询结果从tuple类型转化为list类型，且list中每一个元素都是一个字典，key名与数据库表的列名对应，value与数据库中记录的取值。
        :param table:查询结果所在的表名。
        :param data_tuple:需要转化类型的数据。
        :return:转化为list类型后的数据。
        """
        column_name_tuple = self.__get_column_name__(table = table, database=database)
        data_list = []
        for data in data_tuple:
            record = {}
            for index in range(0, len(column_name_tuple),1):
                record[column_name_tuple[index][0]] = data[index]
            data_list.append(record)
        return data_list



if __name__ == '__main__':
    db = MySQLDatabaseClass()
    record = {}
    record['post_doctor_url'] = 'http://club.xywy.com/doc_card/47794488/blog'
    data = db.select(table = 'help_topic_post',record=record)
    print type(data)
    # print data

    for record in data:
        print record
    db.close()
