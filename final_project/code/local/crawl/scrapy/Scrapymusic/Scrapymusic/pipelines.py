# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy import log
from scrapy.exporters import JsonItemExporter
from scrapy import signals
import json
import codecs
    
class JsonWithEncodingMusicPipeline(object):
    def __init__(self):
        self.file = codecs.open('C:/Users/Bokkin Wang/data/emotion.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()