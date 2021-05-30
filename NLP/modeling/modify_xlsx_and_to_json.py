import pandas as pd

# 가사 데이터 중 \r 삭제하기 : 필요하실 때 사용하시면 됩니다.
#
# data = pd.read_excel('modeling_result(whole_data).xlsx') # 파일 불러오기
#
# n_list = [] # 빈 리스트 생성
# for i in range(len(data)): # 불러온 데이터 길이만큼 반복문 실행
#     dt = data['Lyric'][i] # lyric 데이터 한 행씩 dt 변수에 담음
#     new = dt.replace('\r', '') # dt(lyric 데이터 한 행)에서 '\r'을 공백('')으로 대체(즉, \r 제거)한 후 new 변수에 담음
#     n_list.append(new) # 빈 리스트인 n_list에 new 변수 추가하기
#
# m_dt = pd.DataFrame(n_list) # 데이터 길이만큼 데이터가 쌓인 n_list를 데이터프레임 형식으로 바꿈(변수명 m_dt)
# m_dt.columns = ['Lyric'] # m_dt의 컬럼명을 Lyric으로 변경 : 컬럼명을 동일시켜주기 위함
#
# data['Lyric'] = m_dt['Lyric'] # m_dt의 Lyric 데이터를 data의 Lyric에 덮어씌우기 : 기존의 data['Lyric']은 사라짐.
#
# data.to_excel('to_json.xlsx', index=False) # 결과물을 엑셀로 저장. index=False는 인덱스 없이 저장한다는 뜻
#
#
#

# 파이썬 객체를 json 파일로 변환하기
import xlrd
from collections import OrderedDict
import json

# 참고 블로그 : https://pjs21s.github.io/json-studying/

excel_path = 'to_json.xlsx'  # json으로 변환하고 싶은 데이터가 있는 주소
# 현재 excel_path는 py가 있는 파일에 xlsx도 있으므로 어떠한 주소 없이 파일명만 적어도 됨
wb = xlrd.open_workbook(excel_path) # 해당 주소에 있는 파일(excel_path)을 여는 코드
sh = wb.sheet_by_index(0) # sheet_by_index(index) : sheet index 번호로 가지고 오기

data_list = []

for rownum in range(1, sh.nrows): # 1부터 인덱스 끝까지, 즉 전체 데이터 길이만큼 반복문 실행
    data = OrderedDict() # 형식 지정 / OrderDict : 기본 딕셔너리와 거의 비슷하지만, 입력된 아이템들의 순서를 기억하는 dict임.
    row_values = sh.row_values(rownum) # sheet row 값 읽기

    # print(row_values) # 확인차 출력

    data['song_id'] = int(row_values[0])  # (default : float) -> int형으로 변환

    if type(row_values[1]) == float:  # 만약 value가 float 형이면
        data['song_name'] = str(int(row_values[1]))  # int로 변환 후 str로 변환
    else:
        data['song_name'] = row_values[1]  # 아니면 계속 진행 (기본 str형)

    data['artist'] = row_values[2]
    data['album'] = row_values[3]
    data['Like_count'] = int(row_values[4])  # float -> int형 변환
    data['genre'] = row_values[5]
    data['Lyric'] = row_values[6]
    data['cover_url'] = row_values[7]

    data['keyword_situation'] = row_values[8].split(', ')  # python : list -> json : array
    if data['keyword_situation'] == ['']: # 만약 해당 데이터가 ['']라면
        data['keyword_situation'] = [] # []으로 변경
    else:
        data['keyword_situation'] = row_values[8].split(', ') # list에서 array로 바꾸기만 하기

    data['keyword_emotion'] = row_values[9].split(', ')
    if data['keyword_emotion'] == ['']:
        data['keyword_emotion'] = []
    else:
        data['keyword_emotion'] = row_values[9].split(', ')

    data['keyword_place'] = row_values[10].split(', ')
    if data['keyword_place'] == ['']:
        data['keyword_place'] = []
    else:
        data['keyword_place'] = row_values[10].split(', ')

    data['keyword_season'] = row_values[11].split(', ')
    if data['keyword_season'] == ['']:
        data['keyword_season'] = []
    else:
        data['keyword_season'] = row_values[11].split(', ')

    data['keyword_weather'] = row_values[12].split(', ')
    if data['keyword_weather'] == ['']:
        data['keyword_weather'] = []
    else:
        data['keyword_weather'] = row_values[12].split(', ')

    data_list.append(data) # data_list라는 리스트 맨 뒤에 data 추가하기

# 파이썬 객체를 json 파일로 저장하기
j = json.dumps(data_list, ensure_ascii=False) #, allow_nan=False)
# ensure_ascii : 한글 정상표시를 위해 필수
# allow_nan : nan(결측치) 허용 여부, defaut = True
with open('rf_result_data.json', 'w', -1, "utf-8") as f:
    # open( '저장명.json', 'w'(write), -1, 'utf-8'(한글) ) as 약자(생략 가능)
    f.write(j)

# print(j)


# 이후 json 데이터 정리하는 사이트에서 데이터 정리하기!
# -> https://jsonlint.com/