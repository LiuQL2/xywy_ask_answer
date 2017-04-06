#!/usr/bin/env python
# -*-coding: utf-8 -*-

'''
用来读取sqlite数据库中的文件。
'''

# Author: Liu Qianlong <LiuQL2@163.com>
# Date: 2016.10.24


import sys
import sqlite3
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


class SQLiteDatabaseClass(object):
    def __init__(self, file_path):
        """
        初始化一个实例。
        :param file_path: sqlite数据库文件的路径需要确定到文件名称，如：'D:/Qianlong/Liuan/xywy.db3'。
        """
        self.file_path = file_path
        self.__connection = None
        self.__cursor = None

    def connect(self):
        """
        连接sqlite数据库文件。
        :return: 不返回数据。
        """
        self.__connection = sqlite3.connect(database=self.file_path)

    def insert(self, table, record):
        """
        向数据库表中插入数据
        :param table:需要插入的数据库表
        :param record:需要插入的数据，一个记录，必须为字典，key为数据库表列名。
        :return:Nothing to return.
        """
        try:
            sql1 = 'insert into ' + table + ' ('
            sql2 = 'values ('
            values = []
            for (key, value) in record.items():
                sql1 = sql1 + key + ','
                sql2 = sql2 + "'%s',"
                values.append(value)
            sql1 = sql1[0:len(sql1) - 1] + ') '
            sql2 = sql2[0:len(sql2) - 1] + ') '
            sql = sql1 + sql2
            sql = sql % tuple(values)
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(sql)
            self.__connection.commit()
            self.__cursor.close()
        except Exception,e:
            print traceback.format_exc(), e.message

    def delete(self,table,record):
        """
        删除数据库表中的数据。
        :param table: 表名
        :param record: 需要删除的记录。为字典，key为列名。
        :return: 没有返回。
        """
        sql = 'delete from ' + table + ' where '
        values = []
        for (key, value) in record.items():
            sql = sql + key + " = '%s' and "
            values.append(value)
        sql = sql[0:len(sql) - 5]
        sql = sql % tuple(values)
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql)
            self.__connection.commit()
            cursor.close()
        except Exception, e:
            print traceback.format_exc(), e.message

    def update(self,table, record, primary_key):
        """
        更新数据库表中的记录。
        :param table: 表名
        :param record: 需要更新的新的数据，是字典，key为列名。
        :param primary_key: 需要更新的记录的主键，根据这个主键进行寻找记录。是一个字典，key为列名。
        :return: Nothing to return.
        """
        sql1 = 'update ' + table + ' set '
        sql2 = ' where '
        values = []
        for (key, value) in record.items():
            sql1 = sql1 + key + " = '%s',"
            values.append(value)
        for (key, value) in primary_key.items():
            sql2 = sql2 + key + " = '%s' and "
            values.append(value)
        sql1 = sql1[0:len(sql1) - 1]
        sql2 = sql2[0:len(sql2) - 5]
        sql = sql1 + sql2
        sql = sql % tuple(values)
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql)
            self.__connection.commit()
            cursor.close()
        except Exception,e:
            print traceback.format_exc(), e.message

    def select(self, table, size = None):
        """
        数据库中读取操作。
        :param table: 需要读取数据的表名，不能为空。
        :param size: 需要返回数据的数量，100表示返回100条记录，可以为空，表示返回表table中的全部数据。
        :return: 返回查询数据的结果。
        """
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('select * from '+ table + ';')
        if size == None:
            data_tuple = self.__cursor.fetchall()
        else:
            data_tuple = self.__cursor.fetchmany(size=size)
        self.__cursor.close()
        return self.__tuple_to_dict__(data_tuple, table= table)

    def create_table(self, table_name, column_names, column_types, not_null = [],primary_key=[]):
        """
        创建数据库表
        :param table_name: 表名，string
        :param column_names: 列名，list，包含所有列名
        :param column_types: 列的类型，list, 长度与列数相同。应该只有四种['INTEGER','TEXT','REAL','BLOB']，
        :param not_null: 不为空的列名，list，默认为空list
        :param primary_key: list,里面包含设为主键的列名， 默认为空list
        :return: None
        """
        sql = "create table " + table_name + " ( "
        for column in column_names:
            # 判断哪些属性不为空
            if column in primary_key or column in not_null:
                sql = sql + column + " " + column_types[column_names.index(column)] + " NOT NULL,"
            else:
                sql = sql + column + " " + column_types[column_names.index(column)] + ","
        #添加主键。
        if primary_key == None:
            sql = sql[0:len(sql) - 1] + ");"
        else:
            sql = sql + "primary key ("
            for key in primary_key:
               sql = sql +  key + ","
            sql = sql[0:len(sql) - 1] + "));"
        try:
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(sql)
            self.__connection.commit()
            self.__cursor.close()
        except Exception, e:
            print traceback.format_exc(), e.message

    def table_info(self,table):
        """
        用于表结构的查询操作。
        :param table: 需要查询的表，不能为空。
        :return: 返回表的结构。
        """
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('PRAGMA table_info('+ table +');')
        info = self.__cursor.fetchall()
        self.__cursor.close()
        return info

    def table_column(self, table):
        table_info = self.table_info(table = table)
        column_name = []
        for column in table_info:
            column_name.append(column[1])
        return column_name

    def __tuple_to_dict__(self, data, table):
        data_list = []
        table_column = self.table_column(table=table)
        for line in data:
            record = {}
            for index in range(0, len(table_column), 1):
                record[table_column[index]] = line[index]
            data_list.append(record)
        return data_list

    def close(self):
        """
        关闭数据库的连接。
        :return: 无返回数据。
        """
        self.__connection.close()


if __name__ == '__main__':
    # database = SQLiteDatabaseClass('D:/Workspace/JavaProjects/gephi-toolkit-demos-master/src/main/resources/org/gephi/toolkit/demos/lesmiserables.sqlite3')
    database = SQLiteDatabaseClass('C:/Users/LiuQL/Desktop/lesmiserables.sqlite3')
    database.connect()
    values = database.select(table='edges',size=100)
    for record in values:
        print record
        for (key, value) in record.items():
            print key, value
    database.create_table(table_name='edge3',column_names=['id','label', 'source'],column_types=['INTEGER','TEXT','REAL'], not_null=['source', 'label'],primary_key=['id', 'label'])
    database.insert(table='edge3', record={'id':2,'label':'qianlong', 'age':3.5,'boolean':True})
    database.update(table='edge3',record={'label':'Qianlong', 'age':24, 'boolean':'yes'}, primary_key={'id':2, 'label':'Qianlong Liu'})
    database.delete(table='edge3',record={'label':'Qianlong', 'age':24, 'boolean':'yes'})

    database.close()