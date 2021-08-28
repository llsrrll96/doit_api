from flask_restful import Resource
from flask import Flask,request

class Category_Controller(Resource):
  def __init__(self, **kwargs):  # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
    self.category = kwargs['category']

  def get(self): # 사용 x
    return {'result':"None"},200 #Status Code

  def post(self):
    hsk_list =request.get_json()
    hsk_list = hsk_list['hscodes']
    print("카테고리 데이터 받음:",hsk_list)
    return self.category.search_category(hsk_list)
