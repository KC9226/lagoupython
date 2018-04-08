# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.cookies import CookieJar
from scrapy.http import Request
import urllib.parse
import uuid
import time
import json
from lagoupython.items import LagoupythonItem
from scrapy.http import response


class JdpythonSpider(scrapy.Spider):
    name = 'jdpython'
    allowed_domains = ['lagou.com']
    # start_urls = ['https://www.lagou.com/jobs/list_python?px=default&city=上海#filterBox']
    start_urls = ['https://www.lagou.com']
    sessionid = ''
    cookies = {}
    post_dict = {}
    headers = {
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
    }

    def parse(self, response):
        # item_list = Selector(response=response.text).xpath('//li[@id="con_list_item default_list"]')
        # print(item_list)
        print(response)
        # print(response.text)
        cookie_jar = CookieJar()  # 对象，中封装了 cookies
        cookie_jar.extract_cookies(response, response.request)  # 去响应中获取cookies
        # self.sessionid = ''
        for k, v in cookie_jar._cookies.items():
            # print(cookie_jar.__dict__)
            # print(k, v)
            for i, j in v.items():
                # print(i, j)
                for m, n in j.items():
                    # print(m, n.value)
                    self.sessionid = n.value
        #             self.cookie_dict[m] = n.value
        #     print(self.sessionid)

        self.cookies = {'JSESSIONID': str(self.sessionid),
                        '_gat': '1',
                        # 'user_trace_token': '20170203041008-9835aec2-e983-11e6-8a36-525400f775ce',
                        'user_trace_token': time.strftime("%Y%m%d%H%M%S") + '-' + str(uuid.uuid4()),
                        'PRE_UTM': '',
                        'PRE_HOST': '',
                        'PRE_SITE': 'https%3A%2F%2Fwww.lagou.com%2F',
                        'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D',
                        'LGUID': time.strftime("%Y%m%d%H%M%S") + '-' + str(uuid.uuid4()),
                        'SEARCH_ID': str(uuid.uuid4()).replace('-', ''),
                        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522248605,1522287386',
                        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': str(time.time().__int__()),
                        '_ga': 'GA1.2.2140793913.1522248605',
                        '_gid': 'GA1.2.1478362998.1522248605',
                        'LGSID': time.strftime("%Y%m%d%H%M%S") + '-' + str(uuid.uuid4()),
                        'LGRID': time.strftime("%Y%m%d%H%M%S") + '-' + str(uuid.uuid4()),
                        'index_location_city': '%E4%B8%8A%E6%B5%B7',
                        'TG-TRACK-CODE': 'index_search',
                        }

        self.post_dict = {
            'first': 'true',
            'pn': '1',
            'kd': 'python'
        }
        yield Request(
            url="https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false",
            method='POST',
            cookies=self.cookies,
            body=urllib.parse.urlencode(self.post_dict),
            headers=self.headers,
            callback=self.parse1
        )
        pass

    def parse1(self, response):
        # print('parse1', response.text, type(response.text))
        job_data = json.loads(response.text)
        # print(job_data['content']['positionResult']['result'])
        for per_item in job_data['content']['positionResult']['result']:
            pyjob_item = LagoupythonItem()
            pyjob_item['positionName'] = per_item['positionName']
            pyjob_item['companyShortName'] = per_item['companyShortName']
            pyjob_item['salary'] = per_item['salary']
            yield pyjob_item

        totalCount = job_data['content']['positionResult']['totalCount']
        pageNo = job_data['content']['pageNo']
        pageSize = job_data['content']['pageSize']
        x = totalCount // pageSize
        y = totalCount / pageSize
        if x < y:
            pageSum = x + 1
        else:
            pageSum = x
        if 1 <= pageNo <= pageSum:
            tmp = {'first': 'false', 'pn': pageNo + 1}
            self.post_dict.update(tmp)
            yield Request(
                url="https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false",
                method='POST',
                cookies=self.cookies,
                body=urllib.parse.urlencode(self.post_dict),
                headers=self.headers,
                callback=self.parse1
            )
            pass
        # 获取新闻列表
        # yield Request(url='http://dig.chouti.com/', cookies=self.cookie_dict, callback=self.parse3)

