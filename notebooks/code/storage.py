# provide a storage interface for data
# assumes config.py contains credential and DB information

from sqlalchemy import create_engine
import config

class Storage :
	
	def __init__(self, connPre='mysql+pymysql://') :
		connectStr = connPre + config.DB_USER + ":" + config.DB_PASS + "@" + config.DB_HOST +  "/" + config.DB_NAME
		try:
			self.db_engine = create_engine(connectStr)
		except Exception as ex:
			print(ex)
			self.db_engine = -1

	
	
