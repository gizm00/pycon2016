# Sub class of Data.py for scraped data

import pandas as pd 
import config
import requests
from classes.Data import Data
import numpy as np
from classes import Utilities

class DistanceMergeData(Data):

	# storage param is expected to be of type classes.Storage
	# IMPORTANT! df_list as an ORDERED list of data frames to merge
	# data frames are merged in pairs starting with df_list[0] and df_list[1]
	# i.e. 
	# m1 = merge(df_list[1], df_list[0], how=left)
	# m2 = merge(df_list[2], m1, how=left)
	# m3 = merge(df_list[3], m2, how=left)


	def __init__(self, name, df_list,storage):
		self.df = pd.DataFrame()
		self.storage = storage
		self.name = name
		if (len(df_list) < 2):
			print("DistanceMergeData.__init__: must pass df_list with length of 2 or greater")
			return

		self.df_list = df_list

	def run_merge(self, df_sub, df_super):
		merge_idx = Utilities.get_merge_index(df_sub,df_super, 0.01)
		df_super = df_super.assign(merge_index=merge_idx.astype(int))
		df_sub = df_sub[df_sub.columns[~df_sub.columns.isin(df_super.columns)]]
		merged = pd.merge(df_super, df_sub, how='left', left_on='merge_index', right_index = True)
		return merged

	def extract(self):
		df_super = self.df_list[1]
		df_sub = self.df_list[0]
		merged = run_merge(df_sub, df_super)
		self.df = self.df.append(merged)

		if len(df_list > 2) :
			# continue merge process
			for i in range(2,len(df_list)):
				df_sub = self.df
				df_super = df_list[i]
				merged = run_merge(df_sub, df_super)
				self.df = self.df.append(merged)




	def put(self):
		if (self.df.empty) :
			print("DistanceMergeData.put(): dataframe is empty, run get() or extract()")
			return
		self.storage.put(self.df, self.name)

	def get(self) :
		self.df = self.storage.get(self.name)

