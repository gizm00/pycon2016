# subclass of camping_data.Data for reading RIDB
import requests
import pandas as pd
import config
from camping import camping_data
from geopy.distance import vincenty
import itertools
import numpy as np
import config

class RidbData(camping_data.WebData):
		
	def get(self):
		# comment these out to use the real deal post tutorial
		#facilities_params = dict(apiKey=config.RIDB_API_KEY, state='OR', activity=activity_id, limit=limit, offset=0)
		#facilities_resp = requests.get(url=facilities_url, params=facilities_params)

		request_url = "http://" + config.LAMP_IP + '/ridb_mock.json'
		self.web_data = pd.read_json(request_url)

	def extract(self):
		if self.web_data.empty:
			print("RidbData.extract(): self.web_data undefined. Run get() first")
			return

		# in this example the extraction is the web_data
		self.df = self.web_data

	def vincenty_matrix(group):
	    group_matrix = pd.DataFrame(index = group.index, columns = group.index)  
	    for c in group_matrix.columns:
	        lat1 = group.columns.get_loc("FacilityLatitude")
	        long1 = group.columns.get_loc("FacilityLongitude")
	        lat2 = group.FacilityLatitude[c]
	        long2 = group.FacilityLongitude[c]
	        group_matrix[c] = group.apply(lambda x: vincenty((x[lat1], x[long1]), (lat2,long2)).miles, axis=1)
	    return group_matrix.as_matrix()
