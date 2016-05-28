# Sub class of RidbData to implement live API
from classes.RidbData import RidbData
import pandas as pd
import json
from pandas.io.json import json_normalize
import requests

class RidbDataLive(RidbData) :

	def extract(self):
		try:
			response = requests.get(url=self.endpoint,params=self.url_params)

		except Exception as ex:
			print("RidbDataLive.extract(): unable to get request " + self.endpoint)
			print("with params: " + str(self.url_params))
			print(ex)
			self.df = pd.DataFrame()
			return

		try :
			data = json.loads(response.text)
			self.df = json_normalize(data['RECDATA'])


		except Exception as ex:
			print("RidbData.extract(): unable to read response")
			print(ex)

		super().clean()