# Sub class of Data.py for the RIDB API

import pandas as pd 
import config
import requests
import json
from classes.Data import Data
from pandas.io.json import json_normalize

class RidbData(Data):

	#dict_params = dict(apiKey = Config.RIDB_API_KEY)
	def __init__(self, name, activity_name, dict_params):
		self.endpoint = config.RIDB_ENDPOINT
		self.activity = activity_name
		self.url_params = dict(apiKey = config.RIDB_API_KEY)
		self.name = name
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

