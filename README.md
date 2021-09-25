# doit_api
- 빅리더 AI 아카데미 프로젝트 AI을 활용한 HS코드 추천 서비스 / flask 서버 구현


![image](https://user-images.githubusercontent.com/58140426/134754233-e5614924-4287-428e-9da2-f89c0d274175.png)

<br><br>
![image](https://user-images.githubusercontent.com/58140426/134754306-40ac029e-c94c-4a7f-b722-0ebfb04d3bb1.png)
- HS코드 검색을 위해서 HS 코드에 대한 각 카테고리 내용을 하나의 sentence 로 합쳐서 한 속성으로 만들었다.
<br>
<br>

![image](https://user-images.githubusercontent.com/58140426/134754321-fb1f7368-8ae8-4c3f-8074-cc2ff39ffa75.png)
- 앞서 생성한 카테고리 내용 sentence 는 속성명을 'cate_sentence' 으로 두고 <b>실제 품목분류사례명</b>을 속성명 'sentence'로 두어 
2개의 속성 ('sentence', 'cate_sentence')을 가진 <b>HS 코드 검색 테이블</b>을 구성하였다.
