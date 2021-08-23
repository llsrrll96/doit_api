from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask import Flask, jsonify, request

class Find_Controller(Resource):
    def __init__(self,**kwargs): # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
        self.search = kwargs['search']

    def post(self):
        json_data = request.get_json(force=True)
        names = json_data['names']

        # 리스트를 이용하여 찾는 메소드

        print(jsonify(nm=names))
        return jsonify(nm=names)

    def get(self,name):
        return self.search.search_name_hscode(name)