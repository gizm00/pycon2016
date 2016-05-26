# Sub class of Data.py for the RIDB API

import pandas as pd 
import config
import requests
import json
from classes.Data import Data
from pandas.io.json import json_normalize

class RidbData(Data):

	# RIDB API specific information
	activity_dict = dict(camping=9, hiking=14)
	endpoint = config.RIDB_ENDPOINT
	self.url_params = dict(apiKey = config.RIDB_API_KEY)

	def __init__(self, activity, dict_params):
		super()__init__('ridbdata')

		try:
			self.activity_id = self.activity_dict(activity)
		except Exception as ex:
			print("RidbMtHoodFacilities.__init__(): cannot find activity: " + activity)
			print("Activity options are " + self.activity_dict.keys)
			print(ex)
			return

		self.url_params.update(dict(activity_id = self.activity_id))
		self.url_params.update(dict_params)

	def extract(self):
		try :

			response = requests.get(url=self.endpoint + "/" + self.activity, params=self.url_params)
		except Exception as ex:
			print("RidbData.extract(): unable to get request " + self.endpoint + "/" + self.activity)
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

