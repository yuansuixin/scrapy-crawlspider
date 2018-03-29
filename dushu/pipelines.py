# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymysql
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings


class DushuPipeline(object):
    def open_spider(self, spider):
        self.fp = open('book.txt', 'w', encoding='utf8')

    def process_item(self, item, spider):
        obj = dict(item)
        string = json.dumps(obj, ensure_ascii=False)
        self.fp.write(string + '\n')
        print('&' * 30)
        return item

    def close_spider(self, spider):
        self.fp.close()


# class DushuMongoPipeline(object):
#     def open_spider(self, spider):
#         self.conn = MongoClient(host='127.0.0.1', port=27017)
#         db = self.conn.dushu
#         self.mysheet = db.book
#         print('写入MongoDB**********************')
#
#     def close_spider(self, spider):
#         self.conn.close()
#
#     def process_item(self, item, spider):
#         self.mysheet.insert(dict(item))


class DushuMysqlPipeline(object):
    def open_spider(self, spider):
        # 连接数据库
        settings = get_project_settings()
        # 获取配置信息
        host = settings['DB_HOST']
        port = settings['DB_PORT']
        user = settings['DB_USER']
        pwd = settings['DB_PWD']
        dbname = settings['DB_NAME']
        charset = settings['DB_CHARSET']
        self.conn = pymysql.Connect(host=host, port=port, user=user, password=pwd, db=dbname, charset=charset,use_unicode=True)
        print('连接数据库成功,&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


    def process_item(self, item, spider):
        sql = 'insert into book(image_url, name, author, price) values("%s","%s","%s","%s")' % (item['book_image_url'], item['book_name'], item['book_author'], item['book_price'])
        print('43567890')
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            print('写入数据库*********************')
        except Exception as e:
            self.conn.rollback()
        return item
    def close_spider(self, spider):
        self.conn.close()