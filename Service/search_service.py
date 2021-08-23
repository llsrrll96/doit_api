import pandas as pd
from Repository import database

class Search:

    def __init__(self,df):
        self.df = df # app.py 에서 불러옴
        print('database 데이터 받음')

    def show_head(self):
        print(self.df.head())

    def search_name_hscode(self,name):
        new_df = self.df.copy()
        code_list = new_df.loc[new_df['NM'].str.contains(name, na=False)]['HSCODE'].tolist()
        return {'hscodes' : code_list}


