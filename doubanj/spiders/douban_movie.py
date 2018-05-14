# -*- coding: utf-8 -*-
import scrapy
import json
from doubanj.items import DoubanjItem, MovieLoader
# import urllib
# from PIL import Image


class DoubanSpider(scrapy.Spider):
    name = 'douban_movie'
    start_number = 0
    base_url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=7,10&tags=%E7%94%B5%E5%BD%B1&start="
    start_urls = [base_url + str(start_number)]
    # 超过一定的时间之后会被ban,每次只爬200部电影
    max_number = 200
    

    def parse(self, response):
        items = json.loads(response.body)
        for item in items['data']:
            il = MovieLoader(item=DoubanjItem())
            item.pop('star')
            item.pop('cover_x')
            item.pop('cover_y')
            for k, v in item.items():
                il.add_value(k, v)
            yield response.follow(item['url'], self.parse_detail, meta={'key': il})
        # 当返回码异常或者数据为空，不能在继续添加url了，作为停止条件
        if response.status == 200 and len(items['data']) > 0 and self.max_number > 0:
            self.max_number -= 1
            yield response.follow(self.generate_url(), self.parse)

    def generate_url(self):
        self.start_number += 20
        url = self.base_url + str(self.start_number)
        return url

    @staticmethod
    def parse_detail(response):
        il = response.meta['key']
        info = response.xpath('//div[@id="info"]')[0]
        genre = info.xpath('//span[@property="v:genre"]/text()').extract()
        release_time = info.xpath('//span[@property="v:initialReleaseDate"]/text()').extract_first()
        runtime = info.xpath('//span[@property="v:runtime"]/text()').extract_first()
        il.add_value('genre', genre)
        il.add_value('runtime', runtime)
        il.add_value('release_time', release_time)
        yield il.load_item()
