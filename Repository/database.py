import pandas as pd

# 필요 데이터를 합쳐서 반환 하는 클래스
# 요구 데이터가 있을 경우 DataFrame으로 반환해주세요
class DB:
    def get_history_data(self):
        print('database 불러오는 중')
        df_1 = pd.read_csv('Repository/all_products_v3_39999.csv', encoding='utf-8-sig')
        df_2 = pd.read_csv('Repository/all_products_v3_40000_.csv', encoding='utf-8-sig')
        df = pd.concat([df_1, df_2])
        df['HSCODE'] = df['HSCODE'].astype('str')
        return df

    def get_category_data(self):
        print('category 파일 불러오는 중')
        df = pd.read_csv('Repository/hsk_category.csv',encoding='utf-8-sig')
        df['HS CODE 10'] = df['HS CODE 10'].astype('str')
        return df.set_index('HS CODE 10')

    def get_hscode_en_ko(self):
        df= pd.read_csv('Repository/all_Combine.csv',encoding='utf-8-sig')
        df['HSCODE'] = df['HSCODE'].astype('str')
        df['HS6'] = df['HS6'].astype('str')
        return df
