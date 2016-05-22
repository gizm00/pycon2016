# Abstract superclass to provide a unified interface for data extraction
import pandas as pd

class Data:

	def __init__(self):
		self.df = pd.DataFrame()

	def extract(self) :
		assert False, 'get extract must be defined'

