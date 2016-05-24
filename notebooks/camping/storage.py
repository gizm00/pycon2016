# provide a storage interface for data
# assumes config.py contains credential and DB information

from sqlalchemy import create_engine
import pandas as pd
import config

class Storage :
	
	# setup database connection to mysql unless otherwise specified
	def __init__(self, connPre='mysql+pymysql://') :
		connectStr = connPre + config.DB_USER + ":" + config.DB_PASS + "@" + config.DB_HOST +  "/" + config.DB_NAME
		print(connectStr)
		try:
			self.db_engine = create_engine(connectStr)
		except Exception as ex:
			print("Storage object failed to initialize")
			print(ex)
			self.db_engine = -1

	# store passed dataframe object as table <name>
	def put(self, df, name, on_exists) :
		try:
			df.to_sql(name, self.db_engine, if_exists=on_exists)
		except Exception as ex:
			print("Storage.put failed")
			print(ex)	

	# return requested query from storage in a dataframe
	def get(self, query_string) :
		try:
			df = pd.read_sql(query_string, self.db_engine, index_col='index')
		except Exception as ex:
			print("Storage.get failed")
			print(ex)
			return pd.DataFrame()
		return df
