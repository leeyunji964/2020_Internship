import numpy as np
import pandas as pd

# 멜론 장르 데이터 가져오기


data = pd.read_excel('./data/조인/bugs_melon_join.xlsx', encoding='utf-8-sig').drop(['Unnamed: 0','Unnamed: 0_x'], axis=1)
# 데이터 불러오기 - 해당 코드를 실행하기 위해서는 melon_crawling.py가 선행되어야 합니다.

a = data['song_name'] + ' ' + data['artist'] # [노래 제목 + 공백(한 칸) + 가수명] 데이터 만들기 = 검색어
search = pd.DataFrame(a) # 데이터프레임 형식으로 변환
search.columns = ['keyword'] # 컬럼명 변경

search_list = list(np.array(search['keyword'].tolist())) # 리스트화

import time
from selenium import webdriver
from bs4 import BeautifulSoup

start = time.time() # 코드 수행시간 측정용

driver = webdriver.Chrome('C://Users//Stbn//PycharmProjects//pythonProject1//chromedriver.exe') # 크롬드라이버 위치
driver.get('https://melon.com') # 해당 url 불러오기 요청
driver.implicitly_wait(1) # ip ban 막기 위해 1초 기다림

title_list = [] # 노래 제목 리스트
genre_list = [] # 노래 장르 리스트

for i in range(500, 1000): # 한 번에 300 - 500개 정도가 ban 안 당하는 것 같음. for문 범위는 조절해가면서 진행
    driver.find_element_by_class_name('ui-autocomplete-input').send_keys(search_list[i])  # 검색창에 검색어 입력
    driver.find_element_by_xpath('//*[@id="gnb"]/fieldset/button[2]/span').click()  # 검색버튼 클릭

    # 여기서부터 try_except 문
    try:
        driver.find_element_by_xpath(
            '//*[@id="frm_songList"]/div/table/tbody/tr[1]/td[3]/div/div/a[1]').click()  # 곡정보 버튼 클릭

        title = driver.find_element_by_xpath(
            '//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[1]').text  # 곡정보에서 제목 정보 text로 가져오기
        title_list.append(title)

        genre = driver.find_element_by_xpath(
            '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]').text  # 곡정보에서 장르 정보 text로 가져오기
        # //*[@id="frm_searchAlbum"]/div/table/tbody/tr[2]/td[3]/div/div/a[1]
        genre_list.append(genre)

    except:  # 오류가 나면 검색창에 있는 검색어를 지우고 다시 검색해야 하는데, 검색어는 직접 지워야 하니까
        # 그냥 다시 멜론 메인 창으로 돌아가야 할 듯..
        ## 아, 아니면 # 검색창에 검색어 입력, # 검색버튼 클릭 여기를 추가해서 해도 될 것 같은데?

        title = search_list[i]
        title_list.append(title) # 타이틀 데이터는 그대로 놔두고

        genre = 'pass' # genre 변수엔 pass 값 넣기
        genre_list.append(genre) # 장르 리스트에 추가

        driver.get('https://melon.com') # 멜론 홈으로 돌아가기 -> 멜론 아이콘을 누르면 다시 홈으로 돌아가니까 아이콘을 누르는 방식으로 코드 수정해도 ok
        driver.implicitly_wait(1)

chart_list = { # dict-key : 컬럼명 : 데이터
    'song_name': title_list,  # 노래제목
    'genre': genre_list # 장르
}

music = pd.DataFrame.from_dict(chart_list, orient='index')
music = music.transpose() # 행과 열 바꾸기

writer = pd.ExcelWriter("폴더 경로/파일명.xlsx")

music.to_excel(writer, sheet_name='1', startrow=1, header=True)

writer.close()