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
        df = pd.read_csv('Repository/category_all.csv',encoding='utf-8-sig')
        df['hscode10'] = df['hscode10'].astype('str')
        df['hs6'] = df['hs6'].astype('str')

        return df

    def get_hscode_en_ko(self):
        print('검색용영어품목명 파일 불러오는 중')
        # df= pd.read_csv('Repository/all_Combine.csv',encoding='utf-8-sig')
        df= pd.read_csv('Repository/검색용영어품목명_v2.csv',encoding='utf-8-sig')
        df['HSCODE'] = df['HSCODE'].astype('str')
        df['HS6'] = df['HS6'].astype('str')
        return df


    def get_tariffEU_data(self):
        print('관세율 파일 불러오는 중')
        df_eu = pd.read_csv('Repository/tariff_hs_EU.csv', encoding='utf-8-sig')
        df_eu['hscode'] = df_eu['hscode'].astype('str')
        df_eu.fillna('-', inplace=True)

        return df_eu

    def get_tariffUSA_data(self):
        print('관세율 파일 불러오는 중')
        df_usa = pd.read_csv('Repository/tariff_hs_US.csv', encoding='utf-8-sig')
        df_usa['hscode'] = df_usa['hscode'].astype('str')
        df_usa.fillna('-', inplace=True)

        return df_usa

    def get_tariffCN_data(self):
        print('관세율 파일 불러오는 중')
        df_cn = pd.read_csv('Repository/tariff_hs_CN.csv', encoding='utf-8-sig')
        df_cn['hscode'] = df_cn['hscode'].astype('str')
        df_cn.fillna('-', inplace=True)

        return df_cn
