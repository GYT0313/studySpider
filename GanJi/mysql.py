# -*- coding: utf-8 -*-
import pymysql
from config import *


class MySQL():
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT,
                 database=MYSQL_DATABASE):
        """
            MySQL初始化
        """
        try:
            self.db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)
    
    def insert(self, table, data):
        """
            插入数据
        """
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()

    def select(self, table, data):
        """
            读取数据
        """
        sql_query = 'select * from %s ' % (table)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()

        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()