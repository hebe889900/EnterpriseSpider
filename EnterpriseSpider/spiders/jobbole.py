# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from EnterpriseSpider.items import *


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    #允许的域名
    allowed_domains = ['blog.jobbole.com']
    #起始的url
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #业务逻辑
    def parse(self, response):
        '''
        1. 获取文章列表页中的文章URL并交给scrapy下载后并解析
        2. 获取下一页的URL并交给scrapy进行下载，下载完成后交给parse
        '''

        #  解析列表页中的所有文章的URL并交给scrapy下载后并解析
        post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        #  提取下一页并交给scrapy进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self,response):
        print("目前爬取的URL是："+response.url)
        #提取文章的具体逻辑
        article_item = JobBoleArticleItem()
        front_image_url = response.meta.get("front_image_url", "")
        #  获取文章标题
        title = response.css('.entry-header h1::text').extract()[0]
        #  获取发布日期
        create_date = response.css('.entry-meta .entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·", "")
        #  获取点赞数
        praise_num = response.css('.vote-post-up h10::text').extract()[0]
        #  获取收藏数
        collect_num = response.css('.post-adds .bookmark-btn::text').extract()[0].split(" ")[1]
        collect_match_re = re.match(r'.*?(\d+).*', collect_num)
        if collect_match_re:
            collect_num = int(collect_match_re.group(1))
        else:
            collect_num = 0
        #  获取评论数
        comment_num = response.css('.post-adds .hide-on-480::text').extract()[0]
        comment_match_re = re.match(r'.*?(\d+).*', comment_num)
        if comment_match_re:
            comment_num = int(comment_match_re.group(1))
        else:
            comment_num = 0

        content = response.css('div.entry').extract()[0]

        article_item["title"] = title
        article_item["create_date"] =create_date
        article_item["praise_num"] = praise_num
        article_item["collect_num"] = collect_num
        article_item["comment_num"] = comment_num
        article_item["front_image_url"] = front_image_url

        yield article_item