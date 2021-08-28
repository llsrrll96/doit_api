
# json 형태로 만드는 클래스
class Product:  # -> json

    def to_product_list_json(self,rowlist,columns):
        # HSCODE, NM_EN, NM_KO 3개 변수 Product 의 리스트를 Json 으로 반환
        # rowlist = [['0123456789', 'english1', 'korean1'],
        #              ['0123456780', 'english2', 'korean2']]
        # columns = ["HSCODE", "NM_EN", "NM_KO"]
        if len(rowlist[0]) == len(columns):
            js = []
            for i in range(len(rowlist)):
                str_ = '`'.join(rowlist[i]).split('`')
                col = '`'.join(columns).split('`')
                dic = {}
                for j in range(len(columns)):
                    dic[col[j]] = str_[j]
                js.append(dic)
            return js
        else:
            return []

    def from_dataframe_to_js(self,new_df):
        js = []
        indexs = new_df.index
        columns = new_df.columns.tolist()
        for index in indexs:

            values = new_df.loc[index, :].tolist()

            dic = {}
            for i in range(len(values)):
                dic[columns[i]] = values[i]

            js.append(dic)
        return js

