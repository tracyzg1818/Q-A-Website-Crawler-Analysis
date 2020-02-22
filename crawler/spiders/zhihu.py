# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from zhihuUserInfo.items import ZhihuuserinfoItem
import re


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 第一个开始用户
    start_user = 'gu-lu-liyan'
    # 查询粉丝或者关注列表里面的用户需要附带的参数
    include_follow = 'data[*].answer_count, articles_count, gender, follower_count, is_followed, is_following, badge[?(type = best_answerer)].topics'
    # 查询个人信息需要附带参数
    include_userinfo = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    # 用户关注的人,用户ID,查询参数，offset与查询的页数有关，limit为20，每页用户数量
    followees_url = 'https://www.zhihu.com/api/v4/members/{user_name}/followees?include={include_follow}&offset={offset}&limit={limit}'
    # 关注者,粉丝
    followers_url = 'https://www.zhihu.com/api/v4/members/{user_name}/followers?include={include_follow}&offset={offset}&limit={limit}'
    # 用户信息URL
    userinfo_url = 'https://www.zhihu.com/api/v4/members/{user_name}?include={include_userinfo}'

    def start_requests(self):
        # 访问第一个用户
        yield Request(url=self.userinfo_url.format(user_name=self.start_user, include_userinfo=self.include_userinfo),
                      callback=self.get_user_info)
        # offset=0,获取第一页的用户
        yield Request(
            url=self.followers_url.format(
                user_name=self.start_user,
                include_follow=self.include_follow,
                offset=0,
                limit=20),
            callback=self.get_followers_parse)

        yield Request(
            url=self.followees_url.format(
                user_name=self.start_user,
                include_follow=self.include_follow,
                offset=0,
                limit=20),
            callback=self.get_followees_parse)

    # 获取用户信息
    def get_user_info(self, response):
        data = json.loads(response.text)
        item = ZhihuuserinfoItem()
        item['name'] = data['name']
        print(item['name'])
        item['articles_count'] = data['articles_count']
        item['favorited_count'] = data['favorited_count']
        item['follower_count'] = data['follower_count']
        item['following_count'] = data['following_count']
        item['thanked_count'] = data['thanked_count']
        item['answer_count'] = data['answer_count']
        item['user_type'] = data['user_type']
        item['voteup_count'] = data['voteup_count']
        item['url_token'] = data['url_token']
        if len(data['headline']) > 40:
            item['headline'] = re.compile('(.+?)<a').findall(data['headline'])[0]
        else:
            item['headline'] = data['headline']
        sex = ['未知', '女', '男']
        item['sex'] = sex[data['gender'] + 1]
        try:
            if data['business']:
                item['business'] = data['business']['name']
            else:
                item['business'] = ''
        except:
            item['business'] = ''
        item['school'] = ''
        item['major'] = ''
        if data['educations']:
            for i in data['educations']:
                for key, value in i.items():
                    if key == 'major':
                        item['major'] = value['name']
                    elif key == 'school':
                        item['school'] = value['name']
    
        if data['locations']:
            item['locations'] = data['locations'][0]['name']
        else:
            item['locations'] = ''

        yield item

        yield Request(
            url=self.followees_url.format(
                user_name=data.get('url_token'),
                include_follow=self.include_follow,
                offset=0,
                limit=20),
            callback=self.get_followers_parse)
        yield Request(
            url=self.followees_url.format(
                user_name=data.get('url_token'),
                include_follow=self.include_follow,
                offset=0,
                limit=20),
            callback=self.get_followees_parse)

    # 获取粉丝信息
    def get_followers_parse(self, response):
        # 防止有些用户没有粉丝
        try:
            followers_data = json.loads(response.text)
            try:
                if followers_data.get('data'):
                    for user in followers_data.get('data'):
                        user_name = user['url_token']

                        yield Request(
                            url=self.userinfo_url.format(
                                user_name=user_name,
                                include_userinfo=self.include_userinfo),
                            callback=self.get_user_info)

                ##判断是否有下一页，如果不是最后一页，继续翻页提取
                if 'paging' in followers_data.keys() and followers_data.get('paging').get('is_end') == False:
                    yield Request(
                        url=followers_data.get('paging').get('next'),
                        callback=self.get_followers_parse)
            except Exception as e:
                print(e, '该用户没有url_token')
        except Exception as e:
            print(e, '该用户没有粉丝')

    def get_followees_parse(self, response):  # 获取关注者的函数
        # 防止有些用户没有关注者
        try:
            followees_data = json.loads(response.text)
            try:
                if followees_data.get('data'):
                    for user in followees_data.get('data'):
                        user_name = user['url_token']  #
                        yield Request(
                            url=self.userinfo_url.format(
                                user_name=user_name,
                                include_userinfo=self.include_userinfo),
                            callback=self.get_user_info)

                if 'paging' in followees_data.keys() and followees_data.get('paging').get('is_end') == False:
                    yield Request(
                        url=followees_data.get('paging').get('next'),
                        callback= elf.get_followees_parse)
            except Exception as e:
                print(e, '该用户没有url_token或者data')
        except Exception as e:
            print(e, '该用户没有粉丝')
