# subclass of camping_data.Data for reading RIDB

import requests
import pandas as pd
#import json
import config
from camping import camping_data

class RidbData(camping_data.WebData):
		
	def get(self):
		# comment these out to use the real deal post tutorial
		#facilities_params = dict(apiKey=config.RIDB_API_KEY, state='OR', activity=activity_id, limit=limit, offset=0)
		#facilities_resp = requests.get(url=facilities_url, params=facilities_params)

		request_url = "http://" + config.LAMP_IP + '/ridb_mock.json'
		self.web_data = pd.read_json(request_url)

	def extract(self):
		if not self.web_data:
			print("RidbData.extract(): self.web_data undefined. Run get() first")
			return
			
		points = itertools.combinations(self.web_data[['FacilityLatitude', 'FacilityLongitude']].as_matrix(), 2) 

