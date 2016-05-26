# Sub class of Data.py for the RIDB API

import pandas as pd 
import config
import requests
import json
from classes.Data import Data
from pandas.io.json import json_normalize
import numpy as np

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

	def extract(self):
		try :

			response = requests.get(url=self.endpoint,params=self.url_params)
		except Exception as ex:
			print("RidbData.extract(): unable to get request " + self.endpoint)
			print("with params: " + str(self.url_params))
			print(ex)
			self.df = pd.DataFrame()
			return

		try :
			data = json.loads(response.text)
			self.df = json_normalize(data['RECDATA'])
			#request_url = "http://" + config.LAMP_IP + '/ridb_mock.json'
			#self.df = pd.read_json(request_url)

		except Exception as ex:
			print("RidbData.extract(): unable to read response")
			print(ex)

		# clean up data after extraction
		self.df = self.df.replace('', np.nan)
		self.df = self.df.drop(['GEOJSON.COORDINATES','GEOJSON.TYPE'], axis=1)

	def put(self):
		if (self.df.empty) :
			print("RidbData.put(): dataframe is empty, run get() or extract()")
			return
		self.storage.put(self.df, self.name)

	def get(self) :
		self.df = self.storage.get(self.name)

