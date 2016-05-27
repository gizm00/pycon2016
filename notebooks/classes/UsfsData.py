# Sub class of Data.py for scraped info from USFS websites

import pandas as pd 
import config
import requests
from classes.Data import Data
import numpy as np

class UsfsData(Data):

	# RIDB API specific information


	# storage param is expected to be of type classes.Storage
	# scraper param is expected to be of type classes.Scraper
	# df param is expected to have columns facilityname and url
	def __init__(self, name, df, storage, scraper):
		self.df = pd.DataFrame()
		self.storage = storage
		self.name = name
		self.url_df = df
		self.scraper = scraper
	

	def extract(self):
		try :
			self.df = self.scraper.scrape(self.url_df)

		except Exception as ex:
			print("UsfsData.extract(): scraper failed")
			print(ex)
			self.df = pd.DataFrame()
			return

	def put(self):
		if (self.df.empty) :
			print("UsfsData.put(): dataframe is empty, run get() or extract()")
			return
		self.storage.put(self.df, self.name)

	def get(self) :
		self.df = self.storage.get(self.name)

