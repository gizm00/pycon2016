# extension of UsfsWebScraper for running on local files for the tutorial

from classes.UsfsWebScraper import UsfsWebScraper
from bs4 import BeautifulSoup

class UsfsWebScraperLocal(UsfsWebScraper):

	def get_soup(self, row): 
		cg_data = open("webfiles/" + row.url,'r').read()
		cg_soup = BeautifulSoup(cg_data, 'lxml')
		return cg_soup