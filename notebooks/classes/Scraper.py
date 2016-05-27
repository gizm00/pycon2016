# Base Scraper class for defining webscraper interface
import pandas as pd

class Scraper():

	def __init__(self):
		self.df = pd.DataFrame()

	# define scrape routine
	# return df
	def scrape(self):
		assert False, "Scraper.scrape must be defined"
