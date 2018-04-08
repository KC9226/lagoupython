# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from openpyxl import Workbook

# 方式一，默认文件，无需修改，执行命令时要指定文件格式scrapy crawl jdpython -o jdpython.csv --nolog
# class LagoupythonPipeline(object):
#     def process_item(self, item, spider):
#         return item


# 方式二，直接运行，scrapy crawl jdpython --nolog，保存为指定文件名

# class LagoupythonPipeline(CsvItemExporter):
#     def __init__(self):
#         self.files = {}
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         print('==========pipeline==========from_crawler==========')
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline
#
#     def spider_opened(self, spider):
#         savefile = open('pythonjd2.csv', 'wb+')
#         self.files[spider] = savefile
#         print('==========pipeline==========spider_opened==========')
#         self.exporter = CsvItemExporter(savefile)
#         self.exporter.start_exporting()
#
#     def spider_closed(self, spider):
#         print('==========pipeline==========spider_closed==========')
#         self.exporter.finish_exporting()
#         savefile = self.files.pop(spider)
#         savefile.close()
#
#     def process_item(self, item, spider):
#         print('==========pipeline==========process_item==========')
#         print(type(item))
#         self.exporter.export_item(item)
#         return item


class LagoupythonPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        # self.ws.append(['positionName', 'companyShortName', 'salary'])

    @classmethod
    def from_crawler(cls, crawler):
        print('==========pipeline==========from_crawler==========')
        pipeline = cls()
        crawler.signals.connect(pipeline.opened_spider, signals.spider_opened)
        crawler.signals.connect(pipeline.closed_spider, signals.spider_closed)
        return pipeline

    def opened_spider(self, spider):
        print('==========pipeline==========opened_spider==========')
        # self.wb = Workbook()
        # self.ws = self.wb.active
        self.ws.append(['positionName', 'companyShortName', 'salary'])

    def closed_spider(self, spider):
        print('==========pipeline==========closed_spider==========')
        self.wb.close()

    def process_item(self, item, spider):
        line = [item['positionName'], item['companyShortName'], item['salary']]
        self.ws.append(line)
        self.wb.save('testjd7.xlsx')
        return item







