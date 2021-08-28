import urllib.request

class Papago:
    # papago API id, pw
    __client_id = "U9UBbQtpSbWt6Mzn6WdC"
    __client_secret = "rHPIy0JgYq"

    def ko_to_en(self,input_str):
        print("한글 --> 영어")
        encText = urllib.parse.quote(input_str)
        data = "source=ko&target=en&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.__client_id)
        request.add_header("X-Naver-Client-Secret", self.__client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()

        if (rescode == 200):
            response_body = response.read()
            en_response_word = response_body.decode('utf-8')

        else:
            print("Papago Error Code:" + rescode)

        if len(en_response_word) != 0:
            input_str = en_response_word[en_response_word.index('translatedText') + 17:en_response_word.index('engineType') - 3]
        print('papago:',input_str.lower())
        return input_str.lower()