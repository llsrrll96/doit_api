from flask_restful import Resource
from flask import Flask,request

class History_Controller(Resource):
  def __init__(self, **kwargs):  # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
    self.history = kwargs['history']

  def get(self, hsk): # hsk = 9033000000'
    js=self.history.search_history(hsk)
    print('history controller get:',js)
    return js

  def post(self):
    return []