# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    praise_num = scrapy.Field()
    collect_num = scrapy.Field()
    comment_num = scrapy.Field()
    front_image_url = scrapy.Field()

