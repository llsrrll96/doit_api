from flask_restful import Resource
from flask import Flask,request

class Item(Resource):
  def get(self, name):
    return {'result':name},200 #Status Code
  def post(self,name):
    data =request.get_json()
    pass

