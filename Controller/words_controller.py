from flask_restful import Resource
from flask import request

from Service.words_service import Words

class Words_Controller(Resource):
    def __init__(self):
        self.words = Words()

    def post(self):
        print('Words_Controler post: ', request.get_data())
        json_data = request.get_json(force=True)
        input = json_data['productName']

        # 번역
        print('input',input)
        input_en = self.words.ko_to_en(input)
        print('input_en',input_en)

        # 문자열을 이용하여 찾는 메소드
        js= self.words.find_hypernyms(input_en)
        print('유사어 찾기 완료',js)
        return js
