from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask import Flask, jsonify, request

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
    def __init__(self,**kwargs): # *args : 변수 갯수 상관 없음, **kwargs : {'키워드':'특정값'} 형태
        self.search = kwargs['search']

    def post(self):
        json_data = request.get_json(force=True)
        names = json_data['names']
        #args = parser.parse_args()
        #un = str(args['username'])
        #pw = str(args['password'])
        print(jsonify(nm=names))
        return jsonify(nm=names)

    def get(self,name):
        return self.search.search_name_hscode(name)


class HelloWorld(Resource):
    def get(self):
        return {'hello':'world_v2'}