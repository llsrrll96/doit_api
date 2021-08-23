from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from Controller.hello import HelloWorld
from Controller.hello import Test
from Controller.Item import Item
from Controller.find_controller import Find_Controller
import pandas as pd

#Flask 객체 인스턴스 생성
from Repository.database import DB
from Service.search_service import Search

app = Flask(__name__)
api = Api(app)

db = DB()
search =Search(db.get_data())

api.add_resource(Item, '/api/item/<string:name>')

api.add_resource(Test,'/api/test/<string:name>',
                 resource_class_kwargs={'search':search})

api.add_resource(Find_Controller,'/api/search/<string:name>',
                 resource_class_kwargs={'search':search})

api.add_resource(HelloWorld,'/')
# api.add_resource(Dummy, '/', '/index')

if __name__=="__main__":
    app.run()
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)