# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScheduleItem(scrapy.Item):
	term = scrapy.Field()
	link = scrapy.Field()
	subject = scrapy.Field()
	course = scrapy.Field()
	name = scrapy.Field()
	crn = scrapy.Field()