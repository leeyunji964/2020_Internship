import pandas as pd
# 불용어 사전에서 한 글자 단어 삭제하기


data = pd.read_excel('불용어 사전 전처리_real_prototype.xlsx') # 데이터 불러오기

data = data.reset_index() # 데이터 인덱스 리셋
data = data.drop('index', axis=1) # 'index'라는 컬럼 삭제(axis=1) * axis=0이면 행 삭제

word_list = [] # 빈 리스트 생성
for i in range(0, 1381): # 데이터의 처음부터 끝까지, len(data)와 같은 의미. 단 0~1380까지이니까 주의!
    if len(data['word'][i]) >= 2: # data['word']의 길이가 2 이상이면
        word_list.append(data['word'][i]) # 리스트에 추가하기
    else:
        pass # 길이가 2 미만이면 pass(아무것도 하지 않음)

print(word_list) #확인차 출력

df = pd.DataFrame(word_list) # word_list를 데이터 프레임 형식으로 변환
df.columns = ['word'] # 컬럼명을 word로 변경
print(df) # 확인차 출력
df.to_excel('불용어 사전 전처리_real_prototype.xlsx') # 엑셀로 저장
