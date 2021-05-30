import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from konlpy.tag import Okt

# 토큰화한 단어들을 기본형으로 바꿔주기

data = pd.read_excel('music_data_all_final(12-02).xlsx') # 데이터 불러오기
data['stemmed'] = '' #stemmed 라는 빈 column 추가

# 여기서 중요한 건 새로운 리스트에 추가를 하는 게 아니라 해당 단어를 바꾸는 것.

stemming_list = [] # stemming_list라는 빈 리스트 생성
for i in range(len(data)): # 데이터 길이만큼 반복문 실행
    okt = Okt()  # 객체 생성
    text = data['select_sentence_nouns'][i] # select_sentence_nouns 데이터 한 행씩 text 변수에 담기
    filter_text = str(text).replace('.', '').replace(',', ''). \
        replace("'", "").replace('·', ' ').replace('=', '').replace('\n', '')
    # text의 문자들을 공백으로 바꾸기(=제거하기)

    # okt.morphs(데이터, stem=True) : 텍스트를 형태소 단위로 나누는데, 이 때 각 단어에서 어간을 추출함
    stemming = okt.morphs(filter_text, stem=True) #stemming type = list
    stemming_list.append(stemming) # 어간 추출된 단어를 stemming_list 맨 뒤에 추가

    data['stemmed'].loc[i] = stemming_list[i] # stemming_list의 한 행을 data['stemmed'] 컬럼에 덮어씌우기
    # 기존의 data['stemmed'] 데이터는 삭제되고, 그 공간에 stemming_list의 값이 들어감

#print(data) 확인차 출력
data.to_excel('music_data_all_final(12-02).xlsx') # 엑셀로 저장