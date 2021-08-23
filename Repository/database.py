import pandas as pd

class DB:
    def get_data(self):
        print('database 불러오는 중')
        df_1 = pd.read_csv('Repository/all_products_v3_39999.csv', encoding='utf-8-sig')
        df_2 = pd.read_csv('Repository/all_products_v3_40000_.csv', encoding='utf-8-sig')
        df = pd.concat([df_1, df_2])
        return df
