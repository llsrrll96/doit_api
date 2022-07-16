# doit_api
- 빅리더 AI 아카데미 프로젝트 HS 품목 분류 결정 및 추천 서비스 / flask API 서버 구현

![image](https://user-images.githubusercontent.com/58140426/134754954-e8600f98-cc78-47f5-824e-464d16b07736.png)

### 검색 데이터 구축

- 데이터 전처리
  - 검색의 편의성, 검색 속도 향상을 위한 전처리
  - 소문자 변환, 한 글자 단위 제거, 공백처리 / 공백제거, 특수 문자 제거

![image](https://user-images.githubusercontent.com/58140426/134754905-16f861b0-14b8-4cb6-825b-1d7268dc32f4.png)
<br>
<br>

- HS코드 검색을 위해서 HS 코드에 대한 각 카테고리 내용을 하나의 sentence 로 합쳐서 한 속성으로 만들었다.

![image](https://user-images.githubusercontent.com/58140426/134754817-01df8008-5010-4bc4-9315-353c4bc28c55.png)
<br>
<br>

- 앞서 생성한 카테고리 내용 sentence 는 속성명을 'cate_sentence' 으로 두고 <b>실제 품목분류사례명</b>을 속성명 'sentence'로 두어 
2개의 속성 ('sentence', 'cate_sentence')을 가진 <b>HS 코드 검색 테이블</b>을 구성하였다.

![image](https://user-images.githubusercontent.com/58140426/134754321-fb1f7368-8ae8-4c3f-8074-cc2ff39ffa75.png)
<br>
<br>
- spaCy 라이브러리를 활용하여 단어의 기본 형태(The base form)로 변환
- 불용어 제거

![image](https://user-images.githubusercontent.com/58140426/134754990-317e5486-a3c4-4fb2-b579-b5b79ecbdbe1.png)

<br>
<br>

![image](https://user-images.githubusercontent.com/58140426/134755145-88d44c86-6db3-4c81-a0b5-ea2e921cf6a9.png)
<br>
<br>

### 검색 알고리즘
- 각 검색 규칙에 대해 가중치를 두고 , 카테고리 속성 검색 탐색에 대해서도 가중치 부여

![image](https://user-images.githubusercontent.com/58140426/134755200-54d4e37f-0a75-43dc-a201-1c0b86d8f99c.png)
<br>
<br>

### 확장 가능
- 어플리케이션 활용

![image](https://user-images.githubusercontent.com/58140426/134755104-1194edbf-43e3-4c19-8ca3-aaa6264bb9ed.png)
