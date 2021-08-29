from flask_restful import Resource
from flask import Flask,request

class Item(Resource):
  def __init__(self, **kwargs):  # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
    self.search = kwargs['search']

  def get(self):
    # return {'result':"name"},200 #Status Code
    return self.search.search_NM_KO_list()

  def post(self,name):
    data =request.get_json()
    pass

