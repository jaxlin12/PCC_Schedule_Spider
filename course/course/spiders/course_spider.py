import scrapy
import pymongo
from ..items import CourseItem
from scrapy.conf import settings



class CourseSpider(scrapy.Spider):
	name = "course"

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
			)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def start_requests(self):
		for obj in self.collection.find($or: [{"term": "201910"}, {"term":"201930"}]):
			yield scrapy.Request(url=obj['link'], callback=self.parse)

	def parse(self, response):
		item = CourseItem()
		item['link'] = response.url
		sel = scrapy.Selector(response)
		item['capacity'] = sel.xpath('/html/body/table[3]/tr[3]/td[1]/text()').extract_first()
		item['taken'] = sel.xpath('/html/body/table[3]/tr[3]/td[2]/text()').extract_first()
		item['available'] = sel.xpath('/html/body/table[3]/tr[3]/td[3]/text()').extract_first()
		return item