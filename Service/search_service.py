import pandas as pd
from flask import jsonify
import operator
from Domain.product_format import Product
from collections import OrderedDict
from Papago.papago import Papago

# 서비스, 비지니스 메소드 클래스입니다.
# 요구 기능이 있으면 메소드로 만들어서 반환해주세요
# Find_Controller.py 를 통해 클라이언트로 값 전달
# return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

papago = Papago()
product = Product()

class Search:

    def __init__(self,df):
        self.df = df # app.py 에서 불러옴
        print('database 데이터 받음')

    # test
    def show_head(self):
        print(self.df.head())

    # HSCODE, NM_EN, NM_KO 에서 HS6(6단위 hscode 추가)
    def add_HS6(self, new_df): # ->[]
        new_df = new_df.drop_duplicates(['HSCODE'])
        new_df['HS6'] = new_df['HSCODE'].apply(lambda s: s[0:6])
        new_df = new_df[['HS6', 'HSCODE', 'NM_EN', 'NM_KO']]
        return new_df

    def search_NM_KO_list(self): # -> js
        new_df = self.df.drop_duplicates(['NM_KO'])
        print("nm ko list:",new_df.NM_KO.tolist())
        return jsonify(nm_ko_list=new_df.NM_KO.tolist())


    # df 사본으로 복사하여 사용하기
    def search_name_hscode(self,name): # ->js
        df_v = self.df.copy()
        total = {}

        # 영어로 번역
        name = papago.ko_to_en(name)

        # 1순위: 전체 문자열 검색 뽑힌 것
        # 2순위: 한 단어에 대한 갯수에 일치 합으로 기준을 정함
        priority = name
        priority_df = df_v.loc[df_v['NM_EN'].str.contains(priority, na=False)]

        # 단어들을 토큰화
        for tokend_name in name.split():
            extracted_df = df_v.loc[df_v['NM_EN'].str.contains(tokend_name, na=False)]

            indexs = extracted_df['NM_EN'].str.count(tokend_name).index.tolist()
            counts = extracted_df['NM_EN'].str.count(tokend_name).values.tolist()

            for a, b in zip(indexs, counts):
                if a not in total:
                    total[a] = b
                else:
                    total[a] += b
        try:
            # 카운터 평균 구하기
            average = sum(total.values()) / len(total)

            # 정렬
            total = sorted(total.items(), key=operator.itemgetter(1), reverse=True)

            # create total DataFrame
            total_df = pd.DataFrame(columns=['HSCODE', 'NM_EN', 'NM_KO'])
            for t, _ in total:
                if t > average:
                    total_df = total_df.append(df_v.loc[t])

            # # create HS6 to js
            # result_df = self.add_HS6(total_df) # 원래 있음
            total_df = total_df[['HS6', 'HSCODE', 'NM_EN', 'NM_KO']]

            # 상위 10개만 뽑기
            top10_list= list(OrderedDict.fromkeys(total_df.HS6.tolist()))[0:10]
            print(top10_list)
            # 중복 제거, 이미 제거
            # result_df = result_df.drop_duplicates(['HSCODE'])

            # dataframe 으로 뽑아내기
            result_df = pd.DataFrame(columns=['HS6','HSCODE', 'NM_EN', 'NM_KO'])  # 새 dataframe
            result_df = result_df.append(priority_df) # 완전 일치가 1순위
            for hscode6 in top10_list:
                result_df = result_df.append(total_df.loc[total_df.HS6 == hscode6])

            result_df.NM_KO.fillna("-", inplace=True)
            return product.from_dataframe_to_js(result_df)


        except ZeroDivisionError:
            return {
                "code" : "empty",
                "message" : "정보 없음"}


    # hsk(결정세번) 으로 실거래 명들을 반환
    def get_NM_ENs(self,hsk): # -> js
        df_v = self.df.copy()

        # 공백 제거
        df_v['NM_EN'] = df_v.NM_EN.str.strip()
        df_v['NM_KO'] = df_v.NM_KO.str.strip()

        # 마지막에 중복 제거
        df_v = df_v[df_v.HSCODE == hsk].drop_duplicates(['NM_EN'])
        return product.from_dataframe_to_js(df_v)

class Category:
    def __init__(self,cate_df):
        self.cate_df = cate_df
        print('category 데이터 받음')

    def search_category(self,hsk_list):             #  hsk_list=  ["101299000","4814901090"]
        result_df = self.cate_df.loc[hsk_list]
        hscodes = result_df.index.tolist()
        unit_names = result_df.세번10단위품명.tolist()
        divinity_names = result_df['신성질별 분류명'].tolist()

        print('hscodes:',hscodes,'unit_names:',unit_names)
        # json 포멧
        return jsonify(hscodes=hscodes,unit_names=unit_names,divinity_names=divinity_names)

# {
#     "divinity_names": [
#         "말",
#         "기타 종이제품"
#     ],
#     "hscodes": [
#         "101299000",
#         "4814901090"
#     ],
#     "unit_names": [
#         "기타",
#         "기타"
#     ]
# }

class History:
    def __init__(self,history_df):
        self.history_df = history_df

    def search_history(self,hsk): # hsk -> HSCODE,NM,이유,설명
        new_df = self.history_df[self.history_df['HSCODE'].str.contains(hsk)].drop_duplicates(subset=['NM'])
        return product.from_dataframe_to_js(new_df)