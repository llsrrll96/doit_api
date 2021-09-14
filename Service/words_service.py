import urllib.request
import spacy
nlp = spacy.load("en_core_web_sm")
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

wnl = WordNetLemmatizer()

class Words:
    # papago API id, pw
    __client_id = "U9UBbQtpSbWt6Mzn6WdC"
    __client_secret = "rHPIy0JgYq"

    def find_hypernyms(self,input): # 번역된 영어 -> 유사어 str - stream
        results = []
        results.append('검색한 단어(번역) : '+input+'\n')
        words = self.word_to_tokens_without_sw(input).split()

        for name in words:
            if len (name) <= 1: break
            for synset in wordnet.synsets(name)[:5]:
                hypernyms = " ".join(
                    ['"' + hypernym.name().split('.')[0] + '"' for hypernym in synset.hypernyms()])  # 상위어
                hypernyms = hypernyms.replace('_', ' ')
                results.append(hypernyms)
            if len(results) > 1: results.append('\n')  # 값이 있으면
        results = ' '.join(results)
        return results

    # base 단어로 만들고 불용어 제거.
    def word_to_tokens_without_sw(self,text):
        stopwords = nlp.Defaults.stop_words

        doc = nlp(text)
        token_word = [word.lemma_ for word in doc]
        tokens_without_sw = [word for word in token_word if not word in stopwords]
        word_without_sw = ' '.join(tokens_without_sw)
        return word_without_sw

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