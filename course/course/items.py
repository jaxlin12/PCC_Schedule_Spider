# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CourseItem(scrapy.Item):
	capacity = scrapy.Field()
	taken = scrapy.Field()
	available = scrapy.Field()
	link = scrapy.Field()