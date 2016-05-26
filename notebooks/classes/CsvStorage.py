# subclass / implementation of abstract class Storage.py for writing dataframes to csv
# assumes config.py contains credential and DB information

import pandas as pd
import os
from classes.Storage import Storage

class CsvStorage(Storage) :
	
	# setup database connection to mysql unless otherwise specified
	def __init__(self) :
		super().__init__('csv_storage')

	# store passed dataframe object as table <name>
	# NOTE - put overwrites by default
	def put(self, df, name) :
		try:
			df.to_csv(name, Index=False)
		except Exception as ex:
			print("Storage.put failed")
			print(ex)	

	# return requested query from storage in a dataframe
	def get(self, query_string) :
		try:
			df = pd.read_csv(query_string)
		except Exception as ex:
			print("Storage.get failed")
			print(ex)
			return pd.DataFrame()
		return df
