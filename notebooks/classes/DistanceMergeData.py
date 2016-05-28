# Sub class of Data.py for scraped data

import pandas as pd 
import config
import requests
from classes.Data import Data
import numpy as np
from classes import Utilities

class DistanceMergeData(Data):

	# storage param is expected to be of type classes.Storage
	# IMPORTANT! data_list as an ORDERED list of Data objects to merge
	# data objects are merged in pairs starting with data_list[0] and data_list[1]
	# i.e. 
	# m1 = merge(data_list[1].df, data_list[0].df, how=left)
	# m2 = merge(data_list[2].df, m1, how=left)
	# m3 = merge(data_list[3].df, m2, how=left)


	def __init__(self, name, data_list,storage):
		self.df = pd.DataFrame()
		self.storage = storage
		self.name = name
		if (len(data_list) < 2):
			print("DistanceMergeData.__init__: must pass data_list with length of 2 or greater")
			return

		self.data_list = data_list

	def run_merge(self, df_sub, df_super):
		merge_idx = Utilities.get_merge_index(df_sub,df_super, 0.01)
		df_super = df_super.assign(merge_index=merge_idx.astype(int))
		df_sub = df_sub[df_sub.columns[~df_sub.columns.isin(df_super.columns)]]
		merged = pd.merge(df_super, df_sub, how='left', left_on='merge_index', right_index = True)
		return merged

	def extract(self):
		df_super = self.data_list[1].df
		df_sub = self.data_list[0].df
		merged = self.run_merge(df_sub, df_super)
		self.df = self.df.append(merged)

		if len(self.data_list) > 2 :
			# continue merge process
			for i in range(2,len(self.data_list)):
				#df_super = self.df
				#df_sub = self.data_list[i].df
				df_sub = self.df
				df_super = self.data_list[i].df
				merged = self.run_merge(df_sub, df_super)
				self.df = self.df.append(merged)


	def put(self):
		if (self.df.empty) :
			print("DistanceMergeData.put(): dataframe is empty, run get() or extract()")
			return
		self.storage.put(self.df, self.name)

	def get(self) :
		self.df = self.storage.get(self.name)

