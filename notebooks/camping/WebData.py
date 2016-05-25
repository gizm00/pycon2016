# Abstract superclass to provide a unified interface for data extraction
import pandas as pd
from camping.storage import Storage

class WebData():

	def __init__(self, storage_name):
		self.df = pd.DataFrame()
		self.db = Storage()
		self.name = storage_name
		self.web_data = pd.DataFrame()

	# get the info from the web interface
	def get(self) :
		assert False, 'camping_data.Data.get(): extract must be defined'

	# extract info from the web interface
	def extract(self) :
		# fill in with data extraction code
		assert False, 'camping_data.Data.extract(): extract must be defined'

	def store(self):
		# code for storing self.df
		self.db.put(self.df, self.name, 'replace')

	def retrieve(self):
		if self.name:
			query = "select * from " + self.name
			return self.db.get(query)
		else:
			print("camping_data.Data.retrieve(): storage_name is undefined")


