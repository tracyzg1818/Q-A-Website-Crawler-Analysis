# -*- coding: utf-8 -*-
# Define item pipelines
# Don't forget to add the pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime


class ZhihuuserinfoPipeline(object):
    def __init__(self):
        dt = datetime.datetime.now()
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
        )
        conn.query('create database if not exists zhihuUserInfo ')
        conn.commit()
        conn.close()

        self.conn1 = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='zhihuUserInfo',
            charset='utf8')
        self.table_name = dt.strftime('%Y_%m_%d')
        self.conn1.query('drop table if exists ' + self.table_name)
        self.conn1.commit()
        sql_create_table = 'create table ' + self.table_name + '(name char(20),sex char(4),url_token char(40),locations char(30),headline char(40),school char(45),major char(30),business char(30),user_type char(20),answer int(16),articles int(16),follower int(16),following int(16),voteup int(16),thanked int(16),favorited int(16))'
        self.conn1.query(sql_create_table)
        self.conn1.commit()
        self.sql = 'insert into ' + self.table_name + '(name,sex,url_token,locations,headline,school,major,business,user_type,answer,articles,follower,following,voteup,thanked,favorited) values("{name}","{sex}","{url_token}","{locations}","{headline}","{school}","{major}","{business}","{user_type}","{answer_count}","{articles_count}","{follower_count}","{following_count}","{voteup_count}","{thanked_count}","{favorited_count}")'

    def process_item(self, item, spider):

        self.conn1.query(
            self.sql.format(
                name=item['name'],
                sex=item['sex'],
                url_token=item['url_token'],
                locations=item['locations'],
                headline=item['headline'],
                school=item['school'],
                major=item['major'],
                business=item['business'],
                user_type=item['user_type'],
                answer_count=item['answer_count'],
                articles_count=item['articles_count'],
                follower_count=item['follower_count'],
                following_count=item['following_count'],
                voteup_count=item['voteup_count'],
                thanked_count=item['thanked_count'],
                favorited_count=item['favorited_count']
            )
        )
        self.conn1.commit()
        return item

    def close_close(self, spider):
        self.conn1.close()
