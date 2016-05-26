# Base Data class for extracting information from a datasource
import pandas as pd
from classes.Storage import Storage

class Data():

	# input storage is expected to be of type classes.Storage
	def __init__(self, name):
		self.name = name
		self.df = pd.DataFrame()

	def extract(self):
		assert False, "Data.extract must be defined"


