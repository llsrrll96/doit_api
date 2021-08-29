from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from Controller.hello import HelloWorld
from Controller.hello import Test
from Controller.Item import Item
from Controller.find_controller import Find_Controller
from Controller.category_controller import Category_Controller
from Controller.history_controller import History_Controller

#Flask 객체 인스턴스 생성
from Repository.database import DB
from Service.search_service import Search
from Service.search_service import Category
from Service.search_service import History



app = Flask(__name__)
api = Api(app)

db = DB()
search =Search(db.get_hscode_en_ko())
category= Category(db.get_category_data())
history = History(db.get_history_data())

api.add_resource(Category_Controller,'/api/category',
                 resource_class_kwargs={'category':category}) # 초기 데이터를 파라미터로 보내기 위해 쓴다.

api.add_resource(Find_Controller,'/api/search',
                 resource_class_kwargs={'search':search}) # 초기 데이터를 파라미터로 보내기 위해 쓴다.

api.add_resource(History_Controller,'/api/history','/api/history/<string:hsk>',
                 resource_class_kwargs={'history':history}) # 초기 데이터를 파라미터로 보내기 위해 쓴다.

api.add_resource(Item, '/api/item',
                 resource_class_kwargs={'search':search})


api.add_resource(Test,'/api/test/<string:name>',)
api.add_resource(HelloWorld,'/')
# api.add_resource(Dummy, '/', '/index')

if __name__=="__main__":
    #app.run( port="8080") # 로컬 디버깅시, 해당 코드 푸시 금지
    app.run() # 깃허브 마스터로 푸시 할때 사용
    # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)