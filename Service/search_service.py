import collections

import pandas as pd
from flask import jsonify
from Domain.product_format import Product
from Service.words_service import Words
import time
from Repository.database import DB
import spacy
nlp = spacy.load("en_core_web_sm")

# 서비스, 비지니스 메소드 클래스입니다.
# 요구 기능이 있으면 메소드로 만들어서 반환해주세요
# Find_Controller.py 를 통해 클라이언트로 값 전달
# return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

papago = Words()
product = Product()
db = DB()


class Search:

    def __init__(self,df):
        self.df = df # app.py 에서 불러옴

    # test
    def show_head(self):
        print(self.df.head())

    # HSCODE, NM_EN, NM_KO 에서 HS6(6단위 hscode 추가)
    def add_HS6(self, new_df): # ->[]
        new_df = new_df.drop_duplicates(['HSCODE'])
        new_df['HS6'] = new_df['HSCODE'].apply(lambda s: s[0:6])
        new_df = new_df[['HS6', 'HSCODE', 'NM_EN', 'NM_KO']]
        return new_df

    # 자동완성을 위해 한글 거래명 출력
    def search_NM_KO_list(self): # -> js
        print('search_NO_KO_list')
        # 중복제거
        new_df = self.df.drop_duplicates(['NM_KO'])
        new_df['NM_KO'] = new_df['NM_KO'].str.replace(r'[^ㄱ-ㅣ가-힣]+', ' ')
        NM_KO_list = new_df[new_df.NM_KO.str.len() <= 8][new_df.NM_KO.str.len() != 1].NM_KO.tolist()
        print("nm_ko_list", NM_KO_list)
        return jsonify(nm_ko_list=NM_KO_list)


    ################################## 가중치를 이용해서 HS, HSCODE 찾는 함수 #########################################
    # dic : ratio_dict = collections.defaultdict(int)
    # input_df : 찾을 dataframe
    # input : 영문,찾을 문자열
    # column : 검색할 열 = ['sentence', 'cate_sentence']
    def search_to_dic(self, dic, input_df, input, column):  # -> ratio_dict = collections.defaultdict(int)

        # 완전일치
        hscodes = input_df[input_df[column].str.contains(fr'\b{input}\b')].HSCODE
        for hs in set(hscodes):
            dic[hs] += 1

        # 부분일치
        hscodes2 = input_df[input_df[column].str.contains(input)].HSCODE
        for hs in set(hscodes2):
            dic[hs] += 0.8


        ########## 분리 일치 검색 ############
        div = input.split()
        if len(div) >= 2:
            print("2음절 단어")

            wordlist = []
            for word in div:
                if len(word) >= 2:
                    wordlist.append(word)

            if len(wordlist) >= 2:

                # 각각의 단어가 함께 있을 경우
                result1_set = set(
                    input_df[input_df[column].map(lambda x: all(string in x for string in wordlist))].HSCODE)
                # 가중치 합산
                for hs in set(result1_set):
                    dic[hs] += 0.8

                # 단어가 각각 포함돼있는지
                for word in wordlist:

                    # 단어길이 2이상
                    if len(word) >= 2:

                        print('word:', word)
                        # 분리 완전 일치
                        result2_set = set(input_df[input_df['sentence'].str.contains(fr'\b{word}\b')].HSCODE)

                        # 가중치 합산 시작
                        for hs in result2_set:
                            dic[hs] += 0.4

                        # 분리 부분 일치
                        result3_set = set(input_df[input_df[column].str.contains(word)].HSCODE)

                        # 가중치 합산 시작
                        for hs in result3_set:
                            dic[hs] += 0.3

        # 여기서 가중치 전처리 해야될듯

        return dic
    #ratio_dict = collections.defaultdict(int)



    # df 사본으로 복사하여 사용하기
    def search_name_hscode(self,name): # ->js
        start = time.time()

        df_v = self.df.copy()

        # 영어로 번역
        papago_en_word = papago.ko_to_en(name)
        # base 단어로 만들고 불용어 제거.
        en_word = papago.word_to_tokens_without_sw(papago_en_word)

        # 실거래 검색
        ratio_dict = collections.defaultdict(int)
        ratio_dict = self.search_to_dic(ratio_dict, df_v, en_word, 'base_sentence')
        # 카테고리 검색
        ratio_dict = self.search_to_dic(ratio_dict, df_v, en_word, 'base_cate_sentence')
        sorted_dics = sorted(ratio_dict.items(), key=lambda x: x[1], reverse=True)
        print(len(sorted_dics))
        sorted_dics = sorted_dics[0:50]

        # to dataframe
        # 출력
        result_df = pd.DataFrame()
        for hscode, _ in sorted_dics:
            result_df = result_df.append(df_v[df_v.HSCODE == hscode])

        result_df.drop_duplicates(subset='HSCODE',inplace=True)

        try:

            result_df = result_df[['HS6', 'HSCODE']]
            # [] 일때 예외 처리
        except KeyError:
            return {'message': name}
        print("time: ",time.time() - start)
        return product.from_dataframe_to_js(result_df)


    # hsk(결정세번) 으로 실거래 명들을 반환
    def get_NM_ENs(self,hsk): # -> js
        df_v = self.df.copy()

        # 공백 제거
        df_v['NM_EN'] = df_v.NM_EN.str.strip()
        df_v['NM_KO'] = df_v.NM_KO.str.strip()

        # 마지막에 중복 제거
        df_v = df_v[df_v.HSCODE == hsk].drop_duplicates(['NM_EN'])
        return product.from_dataframe_to_js(df_v)


#===============================Category=============================#
class Category:
    def __init__(self,cate_df):
        self.cate_df = cate_df
        print('category 데이터 받음')

    def search_category(self,hsk_list):             #  hsk_list=  ["101299000","4814901090"]
        print('hsk_list:',hsk_list)
        #result_df = self.cate_df.loc[hsk_list]      # hscode 리스트에서 카테고리에 없는 번호가 나왔을때 에러 발생
        result_df = pd.DataFrame(columns=['hs6','hscode10','호','세번10단위품명','신성질별 분류명'])  # 새 dataframe

        for code in hsk_list:
            new_df = self.cate_df[self.cate_df['hscode10'] == code]
            try:
                result_df = result_df.append(new_df)
            except KeyError:
                print('error:', code)  # 추후에 파일 쓰기로 기록하면 좋을 듯

        result_df = result_df.set_index('hscode10')
        hs6 = result_df.hs6.tolist()
        hscodes = result_df.index.tolist()
        hs6content= result_df.호.tolist()
        unit_names = result_df.세번10단위품명.tolist()
        divinity_names = result_df['신성질별 분류명'].tolist()

        print('unit_names:',unit_names)
        # json 포멧
        return jsonify(hs6=hs6,hscodes=hscodes,hs6content=hs6content,unit_names=unit_names,divinity_names=divinity_names)

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

#===============================History=============================#
# 실거래명 찾을때 all_products 사용
class History:
    def __init__(self,history_df):
        self.history_df = history_df

    def search_history(self,hsk): # hsk -> HSCODE,NM,이유,설명
        new_df = self.history_df[self.history_df['HSCODE'].str.contains(hsk)].drop_duplicates(subset=['NM'])

        return product.from_dataframe_to_js(new_df[['HSCODE','NM']])


#===============================Tariff=============================#
class Tariff:
    def __init__(self):
        self.tariff_EU = db.get_tariffEU_data()
        self.tariff_USA = db.get_tariffUSA_data()
        self.tariff_CN = db.get_tariffCN_data()


    def search_tariff(self, hscode, country): #-> json
        if country:
            # hscode -> hs6
            hs6 = int(int(hscode)/10000)
            if country == 'EU':
                print('eu')
                result_df = self.tariff_EU[self.tariff_EU.hs6 == hs6]

                # to list
                hscode = result_df.hscode.tolist()
                product_name = result_df.품명.tolist()
                default_rates = result_df['기본세율'].tolist()
                fta = result_df.FTA.tolist()
                print("EU:",hscode, product_name, default_rates, fta)
                return {'hscode': hscode, 'productname': product_name, '기본세율': default_rates, 'FTA': fta}

            elif country == 'USA':
                print('usa')
                result_df = self.tariff_USA[self.tariff_USA.hs6 == hs6]

                # to list
                hscode = result_df.hscode.tolist()
                product_name = result_df.품명.tolist()
                default_rates = result_df['기본세율'].tolist()
                fta = result_df.FTA.tolist()
                print("USA:",hscode, product_name, default_rates, fta)
                return {'hscode': hscode, 'productname': product_name, '기본세율': default_rates, 'FTA': fta}

            elif country == 'CN':

                # 찾기
                result_df = self.tariff_CN[self.tariff_CN.hs6 == hs6]

                # to list
                hscode = result_df.hscode.tolist()
                product_name = result_df.품명.tolist()
                mfn = result_df['MFN(2순위)'].tolist()
                temp_tax_rates = result_df['잠정세율(2순위)'].tolist()
                apta = result_df['APTA(1순위)'].tolist()
                fta = result_df.FTA세율.tolist()

                print("CN:",hscode, product_name, mfn, temp_tax_rates, apta, fta)

                return {'hscode': hscode, 'productname': product_name, 'MFN': mfn, '잠정세율': temp_tax_rates, 'APTA': apta,'FTA': fta}


#===============================SynWord=============================#
