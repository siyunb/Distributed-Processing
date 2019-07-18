import scrapy
from TravelInfo.items import FindtripItem

class MusicSpider(scrapy.Spider):
    name = 'wangyiyun'
    start_urls = ["http://music.163.com/#/playlist?id=2076290107",
                  'http://music.163.com/#/playlist?id=2076277368',
                  'http://music.163.com/#/playlist?id=2076294506',
                  'http://music.163.com/#/playlist?id=2076311073',
                  'http://music.163.com/#/playlist?id=2076270042',
                  'http://music.163.com/#/playlist?id=2076290107',
                  'http://music.163.com/#/playlist?id=2076210751',
                  'http://music.163.com/#/playlist?id=2076252746',
                 'http://music.163.com/#/playlist?id=2075908456',
                 'http://music.163.com/#/playlist?id=2076083125',
                 'http://music.163.com/#/playlist?id=2075831186',
                 'http://music.163.com/#/playlist?id=2075532617',
                 'http://music.163.com/#/playlist?id=2075700493',
                 'http://music.163.com/#/playlist?id=2075622352',
                 'http://music.163.com/#/playlist?id=2073689723'
                  ]

    def parse(self, response):
        for href in response.xpath('//*[@id="266091621517054661735"]//span[@class="txt"]/a/@href'):
            full_url = response.urljoin(href.extract())
            item = FindtripItem()
            item['emotion'] =response.xpath('//*[@id="auto-id-fhrFfZcoAnqadBO2"]/div[2]/div/div[4]/a[2]/i/text()').extract_first(),
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        content1= "\n".join(response.xpath('//*[@id="lyric-content"]/text()').extract())
        content2="\n".join(response.xpath('////*[@id="flag_more"]/text()').extract())
        item = FindtripItem()
        item['name'] = response.xpath('//body[@id="auto-id-EZLWyixOIRb3AlPh"]//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        item['lyrics'] ="\n".join([content1,content2])