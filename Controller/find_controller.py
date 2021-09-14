from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask import Flask, jsonify, request

class Find_Controller(Resource):
    def __init__(self,**kwargs): # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
        self.search = kwargs['search']

    def post(self):
        print('find controller post: ', request.get_data())
        json_data = request.get_json(force=True)
        names = json_data['productName']
        print('검색어 : ',names) # 봉인 공기

        # 문자열을 이용하여 찾는 메소드
        js= self.search.search_name_hscode(names)
        print('데이터 찾기 완료',js)
        return js

    def get(self):

        return []