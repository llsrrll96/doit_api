from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask import Flask, jsonify, request
import pandas as pd

from Domain.product_format import Product
from Service.search_service import Search

resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep')
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')

#parser = reqparse.RequestParser()
#parser.add_argument('username', type=unicode, location='json')
#parser.add_argument('password', type=unicode, location='json')
# https://stackoverflow.com/questions/25098661/flask-restful-add-resource-parameters

class Test(Resource):
    def __init__(self):
        self.product = Product()
    def post(self):
        json_data = request.get_json(force=True)
        names = json_data['names']
        #args = parser.parse_args()
        #un = str(args['username'])
        #pw = str(args['password'])
        print(jsonify(nm=names))
        return jsonify(nm=names)

    # test
    def get(self,name):
        # HSCODE, NM_EN, NM_KO 3개 변수 Product 의 리스트를 Json 으로 반환
        list_dim2 = [['0123456789', 'korean', '한국어'],
                     ['0123456780', 'korea', '코레아'],
                     ['1000100010', 'holy moly', '홀리몰리 과타몰리'],
                     ['1234567890', 'smart phone', '스마트폰']]
        columns = ["HSCODE", "NM_EN", "NM_KO"]

        js = self.product.to_product_list_json(list_dim2,columns)

        return js


class HelloWorld(Resource):
    def get(self):
        return {'hello':'world_v2'}