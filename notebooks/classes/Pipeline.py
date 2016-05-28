from classes.Data import Data
import pandas as pd 

class Pipeline(Data):
    
    def __init__(self,name, data_list,merge_type,store):
        self.data_list = data_list
        self.name = name
        self.merge_type = merge_type
        self.store = store
        self.df = pd.DataFrame()
        
    def extract(self):
        list(map(lambda x:x.extract(),self.data_list))
        merge = self.merge_type(self.name,self.data_list,self.store)
        
        merge.extract()
        merge.put()
        self.df = merge.df
    
    def put(self):
        if (self.df.empty) :
            print("Pipeline.put(): dataframe is empty, run get() or extract()")
            return
        self.storage.put(self.df, self.name)
    
    def get(self):
        self.df = self.storage.get(self.name)
        