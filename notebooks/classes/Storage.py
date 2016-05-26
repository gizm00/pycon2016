# abstract class for defining a storage inteface

class Storage :
	
	def __init__(self, name) :
		self.name = name

	# store passed dataframe object as table <name>
	def put(self, df, name) :
		assert False, "Storage.put(): needs implementation"

	# return requested query from storage in a dataframe
	def get(self, query_string) :
		assert False, 'Storage.get(): needs implementation'
