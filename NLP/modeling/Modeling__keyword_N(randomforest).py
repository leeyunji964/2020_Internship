import keras
import numpy as np
import pandas as pd
import tensorflow as tf
from numpy import array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

data = pd.read_excel('whole_data_sort(1215).xlsx').drop('Unnamed: 0', axis=1) # 데이터 불러오기
# whole_data_sort(1215).xlsx는 train data와 test data를 합친 엑셀 파일.


# 데이터 정수화
## stemmed data

texts = []
for i in range(len(data)):
    text = data['stemmed'][i].replace(',', '') # 쉼표 제거
    texts.append(text)
# print(texts)

t_sum = 0
for i in range(len(texts)):
    t_sum += len(texts[i])
    avg = t_sum / len(texts)

print("len(texts) 합계 : ", t_sum, ", 평균 : ", avg)

longest_sentence = max(texts, key=len) # 가장 길이가 긴 text
shortest_sentence = min(texts, key=len) # 가장 길이가 짧은 text

# data tokenizing
max_len = len(longest_sentence)

token = Tokenizer()  # tokenizer 객체 생성
token.fit_on_texts(texts)  # 각 단어를 하나의 토큰으로 변환 (단어 인덱스 구축)
word_index = token.word_index  # 단어 인덱스만 가져옴

# tokenizing 결과 확인
print('전체에서 %s개의 고유한 토큰을 찾았습니다.' % len(word_index))
print('word_index type : ', type(word_index))
print('word_index : ', word_index, '\n')

# data sequenceing : str -> int : 각 단어를 빈도순에 따라 인덱싱(오름차순)
words = token.texts_to_sequences(texts)  # 토큰에 지정된 인덱스로 새로운 배열 생성
print('t 0:', texts[0])  # 본래 단어 출력
print('words 0:', words[0], '\n')  # 정수화 된 데이터 출력

# 패딩 : 서로 다른 길이의 데이터 길이를 맞춤. 지정 길이보다 작으면 0으로 채움
padded_x = pad_sequences(words, maxlen=max_len, padding='post')

print('data : ', padded_x)
print('data 0 :', padded_x[0])
print(len(padded_x[0]))
print(token.word_index, '\n')

# 타입 확인
print(type(texts))  # list
print(type(padded_x))  # numpy.ndarray
print(padded_x.shape)  # 5450,1027





# keyword_situation ver.
# 같은 코드이므로 keyword_situation를 keyword_situation을 keyword_emotion,
# keyword_place, keyword_season, keyword_weather로 바꾸면 됨. 맨 마지막에 엑셀로 저장할 때 파일명 유의!
labels = []

for i in range(963): # 라벨이 있는 데이터만
    labels.append(data['keyword_situ'][i])
#print(labels) # 963개

l_sum = 0
for i in range(len(labels)):
    l_sum += len(labels[i])
    l_avg = l_sum / len(labels)
print("len(labels) 합계 : ", l_sum, ", 평균 : ", l_avg)
longest_labels = max(labels, key=len)
shortest_labels = min(labels, key=len)

# data tokenizing
l_max_len = len(longest_labels)

l_token = Tokenizer() # tokenizer 객체 생성
l_token.fit_on_texts(labels) #각 단어를 하나의 토큰으로 변환 (단어 인덱스 구축)
label_index = l_token.word_index # 단어 인덱스만 가져옴

# tokenizing 결과 확인
print('전체에서 %s개의 고유한 토큰을 찾았습니다.' % len(label_index))
print('word_index type : ', type(label_index))
print('word_index : ', label_index, '\n')

#data sequencing : str -> int : 각 단어를 빈도순에 따라 인덱싱(오름차순)
label = l_token.texts_to_sequences(labels) #토큰에 지정된 인덱스로 새로운 배열 생성
print('labels 0:', labels[0]) # 본래 단어 : #분위기, #위로, #감성, #밤, #새벽, #이별
print('label 0:', label[0], '\n') # [5, 11, 1, 6, 12, 3]

#패딩 : 서로 다른 길이의 데이터 길이를 맞춤. 지정 길이보다 작으면 0으로 채움
padded_y = pad_sequences(label, maxlen=len(longest_labels), padding='post') # ndarray

print('padded_labels : ', padded_y)
print('padded_labels 0 :', padded_y[0])
print(len(padded_y[0])) # 100
print(l_token.word_index, '\n')

# 타입 확인
print(type(labels)) # list
print(type(padded_y)) #numpy.ndarray
print(padded_y.shape) # 963, 54




# 데이터 나누기
X_train = padded_x[:963]
y_train = padded_y[:963] # 라벨링 된 데이터만!
X_test = padded_x[964:] # 964부터 끝까지 test data



# modeling - RandomForest
from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import accuracy_score

rf = RandomForestClassifier(random_state=42) # 랜덤포레스트 분류기
rf.fit(X_train, y_train) # train data에 random forest model 학습
# rf_predictions = rf.predict(X_test) # 학습된 모델에 X_test 값을 넣어 y_test 예측 값 생성
# print(rf_predictions)


# 분류기 평가 - gridsearchcv 전 rf model
from sklearn.multioutput import MultiOutputClassifier
# 멀티 출력 가능하게 하는 패키지 설치

rf_classifier = MultiOutputClassifier(rf, n_jobs=1)
rf_classifier.fit(X_train, y_train) # 다중출력이 가능한 모델에 train data 학습

rf_predictions2 = rf_classifier.predict(X_test) # 학습된 모델에 X_test 넣어서 y_test 예측
print(rf_predictions2)

print(rf_classifier.score(X_train, y_train)) # 훈련 데이터 셋 정확도 94.91%


# GridSearchCV : 교차검증과 최적의 파라미터를 동시에 진행
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators':[50,100,200,300],
    'max_depth':[5,10,20]
}

forest_reg = RandomForestClassifier()
grid_search = GridSearchCV(forest_reg, param_grid, cv=5, scoring='neg_mean_squared_error')
print(grid_search.fit(X_train, y_train))

print('최고 평균 정확도 : {0:.4f}'.format(grid_search.best_score_))
print('GridSearchCV 최적 파라미터 : ', grid_search.best_params_)

# 최적의 파라미터로 재진행
best_rf = RandomForestClassifier(n_estimators=50, max_depth=20, random_state=42)
best_rf.fit(X_train, y_train)
brf_predict = best_rf.predict(X_test)
print(brf_predict)

# 다중 출력 가능한 모델
best_rfm = MultiOutputClassifier(best_rf, n_jobs=1)
best_rfm.fit(X_train, y_train)
brfm_prediction = best_rfm.predict(X_test)
print(brfm_prediction)



## Multioutput이 가능한 model : array to list
mt_predicts = brfm_prediction.tolist()
print(mt_predicts)

mo_tagging = data[964:] # 964부터 test data(y)이므로 해당 데이터에 예측 값을 넣기 위함
mo_tagging = mo_tagging.reset_index() # 인덱스 초기화
mo_tagging = mo_tagging.drop('index', axis=1) # 'index'라는 컬럼 삭제(axis=1)

for i in range(len(mt_predicts)): # 데이터 길이만큼 반복문 수행
    mo_tagging['keyword_situation'].loc[i] = mt_predicts[i] # 예측 값을 keyword_situation 컬럼에 덮어씌우기

mo_tagging.head() # 확인

mo_tagging.to_excel('multioutput_rf_situ_result.xlsx') # 엑셀로 저장 * keyword_??? : 저장명 유의!