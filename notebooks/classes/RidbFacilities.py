# Sub class of Data.py for accessing RIDB facility data in a 5 mile radius around MtHood

import pandas as pd 
import config
import requests
import json
from classes.Data import Data
from pandas.io.json import json_normalize

class RidbMtHoodFacilities(Data):
	endpoint = config.RIDB_ENDPOINT + "/facilities"
	params = dict(apiKey = config.RIDB_API_KEY, state='OR', latitude=45.3300, longitude=-121.7089, radius=5)
	activity_dict = dict(camping=9, hiking=14)
	
	def __init__(self, name, activity) :
		self.name = name

		try:
			self.activity_id = self.activity_dict(activity)
		except Exception as ex:
			print("RidbMtHoodFacilities.__init__(): cannot find activity: " + activity)
			print("Activity options are " + self.activity_dict.keys)
			print(ex)

	def extract(self):
		try :
			response = requests.get(url=self.endpoint, params=self.params)
		except Exception as ex:
			print("RidbMtHoodFacilities.extract(): unable to get request " + self.endpoint)
			print("with params: " + str(self.params))
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

