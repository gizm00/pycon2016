# subclass of camping_data.Data for reading RIDB

import requests
import pandas as pd
#import json
import config
from camping import camping_data

class Ridb_Data(camping_data.Data):
		
	def extract(self):
		# comment these out to use the real deal post tutorial
		#facilities_params = dict(apiKey=config.RIDB_API_KEY, state='OR', activity=activity_id, limit=limit, offset=0)
		#facilities_resp = requests.get(url=facilities_url, params=facilities_params)

		request_url = "http://" + config.LAMP_IP + '/ridb_mock.json'
		self.df = pd.read_json(request_url)