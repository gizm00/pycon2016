# Abstract superclass to provide a unified interface for data extraction
import pandas as pd
from camping import storage

class Data:

	def __init__(self):
		self.df = pd.DataFrame()
		self.db = storage.Storage()

	def extract(self) :
		# fill in with data extraction code
		assert False, 'get extract must be defined'

	def store(self, name):
		# code for storing self.df
		self.db.put(self.df, name, 'replace')

	def retrieve(self, query):
		return self.db.get(query)


