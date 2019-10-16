import re

import scrapy
from  sina.items import SinaItem
class SINAjSpider(scrapy.Spider):
    headers = {
        'Host': 'stock.finance.sina.com.cn',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    }
    name = 'xncj'
    def start_requests(self):
        urls = list('http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?t1=3&industry=sw2_110100&symbol=002475&pubdate=2019-10-16&p={0}&qq-pf-to=pcqq.group'.format(x) for x in range(737))
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers)

    def parse(self, response):
        urls = re.findall(r'how/kind/search/rptid/(.*?)">',response.text,re.M)
        st_url = 'http://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/'
        print(urls)
        for url in urls:
            yield scrapy.Request(url=(st_url+url),callback=self.SN,headers=self.headers)


    def SN(self, response):
        item = SinaItem()
        item['title'] = response.xpath('/html/body/div/div[3]/div[1]/div/div/h1/text()').extract()
        item['content'] = response.xpath('/html/body/div/div[3]/div[1]/div/div/div[2]/p/text()').extract()
        item['publish_date'] = response.xpath('/html/body/div/div[3]/div[1]/div/div/div[1]/span[4]/text()').extract()
        item['source'] = response.xpath('/html/body/div/div[3]/div[1]/div/div/div[1]/span[2]/a/text()').extract()
        item['people'] = response.xpath('/html/body/div/div[3]/div[1]/div/div/div[1]/span[3]/a/text()').extract()
        item['type'] = response.xpath('/html/body/div/div[3]/div[1]/div/div/div[1]/span[1]/text()').extract()
        yield item