from flask_restful import Resource
from flask import Flask, jsonify, request

class Tariff_Controller(Resource):
    def __init__(self, **kwargs):  # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
        self.tariff = kwargs['tariff'] # 서비스 객체

    def get(self): # hsk = 9033000000'

        return {
            'message' : 'Tariff GET'
        }

    def post(self):
        json_data = request.get_json(force=True)
        hscode = json_data['hscode']
        country = json_data['country']
        print('hscode : ',hscode,', 국가 :',country) # 봉인 공기
        # service를 통해 불러오기
        js = self.tariff.search_tariff(hscode, country)
        return js

