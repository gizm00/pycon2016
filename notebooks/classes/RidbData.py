# Sub class of Data.py for the RIDB API

import pandas as pd 
import config
import requests
import json
from classes.Data import Data
from pandas.io.json import json_normalize
import numpy as np
from classes import Utilities

class RidbData(Data):

	# RIDB API specific information
	activity_dict = dict(camping=9, hiking=14)
	ridb_endpoint = 'https://ridb.recreation.gov/api/v1'
	endpoint = ridb_endpoint + "/facilities"
	url_params = dict(apiKey = config.RIDB_API_KEY)

	# storage param is expected to be of type classes.Storage
	def __init__(self, name, activity, dict_params, storage):
		self.df = pd.DataFrame()
		try:
			self.activity_id = self.activity_dict[activity]
		except Exception as ex:
			print("RidbData.__init__(): cannot find activity: " + activity)
			print("Activity options are " + self.activity_dict.keys)
			print(ex)
			return

		# update the URL params to include the RIDB Key, activity_id, and input dict_params
		self.url_params.update(dict(activity_id = self.activity_id))
		self.url_params.update(dict_params)
		self.storage = storage
		self.name = name

	def clean(self) :
		self.df = self.df.replace('', np.nan)
		self.df = self.df.dropna(subset=['FacilityLatitude','FacilityLongitude'])
		if 'GEOJSON.COORDINATES' in self.df.columns :
			self.df = self.df.drop(['GEOJSON.COORDINATES'], axis=1)
		if 'GEOJSON.TYPE' in self.df.columns:
			self.df = self.df.drop(['GEOJSON.TYPE'], axis=1)

		# drop duplicates
		#print("dropping duplicates")
		self.df = Utilities.dedupe_by_distance(self.df, 1, 'FacilityLatitude', 'FacilityLongitude', 'LastUpdatedDate')
		#print(self.df.shape)

	def extract(self):
		try :	
			request_url = "http://" + config.LAMP_IP + '/ridb_mock.json'
			self.df = pd.read_json(request_url)
			
		except Exception as ex:
			print("RidbData.extract(): unable to get request " + self.endpoint)
			print("with params: " + str(self.url_params))
			print(ex)
			self.df = pd.DataFrame()
			return

		# clean up data after extraction
		self.clean()
		
	def put(self):
		if (self.df.empty) :
			print("RidbData.put(): dataframe is empty, run get() or extract()")
			return
		self.storage.put(self.df, self.name)

	def get(self) :
		self.df = self.storage.get(self.name)

