from flask import Flask , request
from flask_restful import reqparse, abort, Api, Resource

#  Controller
from Controller.hello import HelloWorld
from Controller.hello import Test
from Controller.Item_controller import Item
from Controller.find_controller import Find_Controller
from Controller.category_controller import Category_Controller
from Controller.history_controller import History_Controller
from Controller.tariff_controller import Tariff_Controller
from Controller.words_controller import Words_Controller

#Flask 객체 인스턴스 생성
from Repository.database import DB
from Service.search_service import Search, Tariff
from Service.search_service import Category
from Service.search_service import History
from werkzeug.serving import WSGIRequestHandler

WSGIRequestHandler.protocol_version = "HTTP/1.1"
app = Flask(__name__)
api = Api(app)

db = DB()
category_data  = Category(db.get_category_data())      # 카테고리 : HS CODE 10,세번10단위품명,신성질별 분류명
search_data =Search(db.get_hscode_en_ko())           # all_Combine : HS6,HSCODE,NM_EN,NM_KO
history_data = History(db.get_history_data())        # HSCODE,NM,이유,설명
tariff_data = Tariff()

api.add_resource(Category_Controller,'/api/category',
                 resource_class_kwargs={'category':category_data}) # 초기 데이터를 파라미터로 보내기 위해 쓴다.

api.add_resource(Find_Controller,'/api/search',
                 resource_class_kwargs={'search':search_data}) # 초기 데이터를 파라미터로 보내기 위해 쓴다.

api.add_resource(History_Controller,'/api/history','/api/history/<string:hsk>',
                 resource_class_kwargs={'history':history_data}) # 초기 데이터를 파라미터로 보내기 위해 쓴다.

api.add_resource(Tariff_Controller,'/api/tariff',
                 resource_class_kwargs={'tariff':tariff_data})

api.add_resource(Words_Controller, '/api/words')

api.add_resource(Item, '/api/item',
                 resource_class_kwargs={'search':search_data})

api.add_resource(Test,'/api/test/<string:name>',)
api.add_resource(HelloWorld,'/')
# api.add_resource(Dummy, '/', '/index')

if __name__=="__main__":
    # app.run( port="8080") # 로컬 디버깅시, 해당 코드 푸시 금지
    app.run() # 깃허브 마스터로 푸시 할때 사용
    # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)
