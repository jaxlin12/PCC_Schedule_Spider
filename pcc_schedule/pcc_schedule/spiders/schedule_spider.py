import logging
import scrapy
import re
import os

from scrapy.http import TextResponse
from ..items import ScheduleItem
from selenium import webdriver
from sys import platform

# set selenium logging level
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.INFO)

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class ScheduleSpider(scrapy.Spider):
	name = 'schedule'
	start_urls = [
				"https://selfservice.pasadena.edu/prod/pw_psearch_sched.p_search",
				]

	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		if platform == "darwin":
			self.driver = webdriver.Chrome(path+"/chromedriver", chrome_options = options)
		elif platform == "win32":
			self.driver = webdriver.Chrome(path+"/chromedriver.exe", chrome_options = options)

	def parse(self, response):
		term_code = scrapy.Selector(response).xpath('//select[@name="term"]/option/@value').extract()
		items = []
		self.driver.get(response.url)
		for code in term_code:
			click_first = self.driver.find_element_by_xpath('//select[@name="term"]/option[@value="{}"]'.format(code))
			click_first.click()
			click_second = self.driver.find_element_by_xpath('//b/input[@type="submit"]')
			click_second.click()
			
			driver_url = TextResponse(url = self.driver.current_url, body = self.driver.page_source, encoding='utf-8')
			sel = scrapy.Selector(driver_url)
			links = sel.xpath('//tr/td[@class="default1"]/a/@href | //tr/td[@class="default2"]/a/@href').extract()
			names = sel.xpath('/html/body/table/tbody/tr/td[18][@class="default1" or @class="default2"]/text() | /html/body/table/tbody/tr[td[@class="default1"]/a[@href]]/td[11][@class="default1"]/text() | /html/body/table/tbody/tr[td[@class="default2"]/a[@href]]/td[11][@class="default2"]/text()').extract()
		
			for link, name in zip(links, names):
				item = ScheduleItem()

				item['name'] = name
				try:
					item['subject'] = re.search('vsub=(.*)&vcrse=', link).group(1)
					item['course'] = re.search('vcrse=(.*)&vterm=', link).group(1)
					item['term'] = re.search('vterm=(\d+)&vcrn=', link).group(1)
					item['crn'] = re.search('&vcrn=(\d+)', link).group(1)
				except:
					print("Find None Match Item")
				item['link'] = "https://selfservice.pasadena.edu/prod/pw_psearch_sched.p_course_popup/?vsub={}&vcrse={}&vterm={}&vcrn={}".format(
																					item['subject'], item['course'], item['term'], item['crn']
																				)
				items.append(item)

			file = "result.txt"
			with open(file, 'a') as f:
				f.write(sel.xpath('/html/body/center/text()').extract_first())
			f.close()
			self.driver.back()

		self.driver.quit()
		return items