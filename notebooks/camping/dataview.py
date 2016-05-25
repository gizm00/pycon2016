# class for creating different views of data

class DataView:

	# data is expected to be of type WebData
	def __init__(self,view_name, data) :
		self.name = view_name
		self.source_data = data

	# method to transform source_data into desired view
	def generate(self) :
		assert False, 'must implement DataView.generate'

	def store(self) :
		assert False 'must implement DataView.store'

	def retreive(self):
		assert False 'must implement DataView.retrieve'
