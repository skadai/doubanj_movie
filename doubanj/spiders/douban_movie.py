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
    # def start_requests(self):
    #     '''
    #     重写start_requests，请求登录页面
    #     '''
    #     return [scrapy.FormRequest("https://accounts.douban.com/login", meta={"cookiejar": 1},
    #                                callback=self.parse_before_login)]
    #
    #
    # def parse_before_login(self, response):
    #     '''
    #     登录表单填充，查看验证码
    #     '''
    #     print("登录前表单填充")
    #     captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
    #     captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
    #     if captcha_image_url is None:
    #         print("登录时无验证码")
    #         formdata = {
    #             "source": "index_nav",
    #             "form_email": "skchang08@126.com",
    #             # 请填写你的密码
    #             "form_password": "sweep537",
    #         }
    #     else:
    #         print("登录时有验证码")
    #         save_image_path = "captcha.jpeg"
    #         # 将图片验证码下载到本地
    #         urllib.urlretrieve(captcha_image_url, save_image_path)
    #         # 打开图片，以便我们识别图中验证码
    #         try:
    #             im = Image.open('captcha.jpeg')
    #             im.show()
    #         except:
    #             pass
    #             # 手动输入验证码
    #         captcha_solution = raw_input('please input the code:')
    #         formdata = {
    #             "source": "None",
    #             "redir": "https://www.douban.com",
    #             "form_email": "skchang08@126.com",
    #             # 此处请填写密码
    #             "form_password": "sweep537",
    #             "captcha-solution": captcha_solution,
    #             "captcha-id": captcha_id,
    #             "login": "登录",
    #         }
    #
    #     print("登录中")
    #     return scrapy.FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]},
    #                                              formdata=formdata,
    #                                             callback=self.parse_after_login)
    #
    # def parse_after_login(self, response):
    #     '''
    #     验证登录是否成功
    #     '''
    #     account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
    #     if account is None:
    #         print("login fail")
    #
    #     else:
    #         print(u"login OK %s" % account)
    #         return scrapy.Request(self.generate_url(), meta={"cookiejar": response.meta["cookiejar"]},
    #                               callback=self.parse)

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
