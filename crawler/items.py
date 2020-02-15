# Define here the models for your scraped items
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuuserinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    answer_count = scrapy.Field()#回答数量
    articles_count = scrapy.Field()#写过的文章数
    follower_count = scrapy.Field()#粉丝数量
    following_count = scrapy.Field()#关注了多少人
    educations = scrapy.Field()#教育背景
    locations = scrapy.Field()#所在地
    url_token = scrapy.Field()#知乎给予的每个人用户主页唯一的ID
    name = scrapy.Field()#用户昵称
    business = scrapy.Field()#一些工作或者商业信息的合集
    user_type = scrapy.Field()#用户类型，可以是个人，也可以是团体等等
    headline = scrapy.Field()#个人主页的标签
    voteup_count = scrapy.Field()#获得的赞数
    thanked_count = scrapy.Field()#获得的感谢数
    favorited_count = scrapy.Field()#被收藏次数
    sex = scrapy.Field()#性别
    school = scrapy.Field()
    major = scrapy.Field()
