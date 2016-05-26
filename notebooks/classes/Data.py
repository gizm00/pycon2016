# Base Data class for extracting information from a datasource
import pandas as pd

class Data():

	def __init__(self, name):
		self.name = name
		self.df = pd.DataFrame()

	def extract(self):
		assert False, "Data.extract must be defined"

