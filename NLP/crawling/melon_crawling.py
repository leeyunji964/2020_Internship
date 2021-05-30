import re
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from pandas import DataFrame
import pandas as pd

# 멜론 시대별 차트 데이터 크롤링 하기 : 노래 고유 번호, 노래 제목, 장르 , 발매일, 앨범명, 가수명, 가사
# 참고 블로그 : https://blog.naver.com/21ahn/221820216442

# 2012년대 노래 시대별 차트
# https://www.melon.com/chart/age/list.htm?idx=1&chartType=YE&chartGenre=KPOP&chartDate=2012&moved=Y
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
# 크롤링 차단 방지용 User-Agent 설정 : 윈도우 용

age_url = "https://www.melon.com/chart/age/list.htm"
# 크롤링할 url

params = { # 파라미터 설정, 여기서 chartDate만 유동적으로 바꿀 수 있게 코드 수정하기
    'idx':'1',
    'chartType':'YE',    #YEAR
    'chartGenre':'KPOP', # 국내음악만
    'chartDate':'2012', #연도설정
    'moved':'Y', # 다음 페이지
}

response = requests.get(age_url, params=params, headers=headers) #url, params, header 데이터를 불러와 url 요청하기(response)
soup = bs(response.text, 'html.parser') # 해당 웹 사이트의 내용을 html.parser를 이용해 soup이라는 변수에 담음
song_list = soup.select('.lst50, .lst100') # 해당 웹 사이트의 내용 중 class가 lst50, lst100인 곳의 데이터를 song_list에 담음

id_list = []     #고유 아이디 리스트
title_list = []  #노래제목 리스트
genre_list = []  #장르 리스트
date_list = []   #발매일 리스트
album_list = []  #앨범 리스트
singer_list = [] #가수 리스트
lyrics = []      #가사 리스트
#like_counts = [] #좋아요 수

for i, meta in enumerate(song_list, 1): # song_list 길이만큼 반복문 수행
    # 순위, 제목
    rank = i # 순위
    try:
        title = meta.select('a[href*=playSong]')[0].text # 해당 구조의 0번 인덱스의 데이터를 title 변수에 담음
    except: # 예외가 발생했을 때 실행하는 코드
        title = meta.select('.wrap_song_info .ellipsis')[0].text
        # class wrap_song_info 아래 class ellipsis의 0번 인덱스 데이터를 title 변수에 담음

    title = title.strip() # title 데이터의 양쪽 공백 제거
    title_list.append(title) # title_list 맨 뒤에 데이터 추가

    # print('\n')
    # print(str(params['chartDate'])+'년')
    # print(str(rank)+ '위.', title)


    # 노래 데이터 url의 html 추출
    song_id_html = str(meta.select('a[onclick*=SongDetail]')) # str(문자)로 데이터 타입 변경
    matched = re.search(r"\'(\d+)\'", song_id_html)
    # re.search() : 정규식 패턴을 검색하고, 첫 번째 항목을 반환.
    # 패턴이 없으면 일치하는 객체를 반환하고 패턴이 발견되지 않으면 null 반환
    song_id = matched.group(1)
    id_list.append(song_id) #고유id 리스트 데이터 추가


    front_url = 'https://www.melon.com/song/detail.htm?songId=' # url 분리 한 것 중 앞 부분
    song_url = front_url + song_id # 전체 url


    # 가수, 앨범명, 발매날짜, 장르
    response = requests.get(song_url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    singer_html = soup.select('.wrap_info .artist a') # 가수 데이터 : class = wrap_info -> class=artist -> a

    # 가수
    singer_s = []
    if len(singer_html) != 0: # 가수 데이터의 길이가 0이 아니라면, 즉 가수 데이터가 존재한다면
        for html in singer_html:
            singer_s.append(html['title']) # singer_s 리스트에 추가
        singer_list.append(singer_s) # singer_list에 추가

    else: # 가수 데이터가 없다면
        # url 없는 various artists용
        singer_html = str(soup.select('.wrap_info .artist')[0]) # str(문자열)로 변경
        singer_html = singer_html.replace('\t','').replace('\r','').split('\n') # \t,\r,\n을 공백으로 대체(=제거)
        singer_html = ''.join(singer_html) # 공백을 기준으로 조인하기
        matched = re.search(r">(.*)<", singer_html)
        singer_s.append(matched.group(1))
        singer_list.append(singer_s)

    # 가수가 여러 명일 때 하나의 string으로 표현
    singer_s = ', '.join(singer_s)
    #singer_list.append(singer_s)


    #앨범명
    album_name_html = str(soup.select('.list dd')[0])
    #matched = re.search(r">(.*)<", album_name_html)
    matched2 = re.search(r">(.*)<", matched.group(1))
    album_name = matched2.group(1).strip()
    album_list.append(album_name)

    #좋아요 수 : 유동적으로 받아오는 시스템이라 인턴 능력으로는 불가
    #like_count_html = str(soup.select('//*[@id="lst50"]/td[5]/div/button/span[2]/text()')) # 결과 X
    #like_count_html = str(soup.select('span#d_like_count'))       #총건수
    # like_count_html = str(soup.select('span#d_like_count.cnt'))n  #총건수
    # like_count_html = str(soup.select('#downloadfrm > div > div > div.entry > '
    #                                   'div.button.d_song_like span.cnt')) #총건수
    #like_count_html = str(soup.select('#btnLike > span.cnt')) # 얘도 총건수
    # like_count_html = str(soup.select('#btnLike > span#d_like_count'))
    # matched = re.search(r">(.*)<", like_count_html)
    # like_count = matched.group(1)
    # like_counts.append(like_count)

    #발매 날짜
    song_date_html = str(soup.select('.list dd')[1])
    matched = re.search(r">(.*)<", song_date_html)
    song_date = matched.group(1)
    date_list.append(song_date)

    #장르
    song_genre_html = str(soup.select('.list dd')[2])
    matched = re.search(r">(.*)<", song_genre_html)
    song_genre = matched.group(1)
    genre_list.append(song_genre)


    # 가사가 있으면 추출
    try:
        lyric_html = str(soup.select('.section_lyric .wrap_lyric .lyric')[0])
        lyric_html = lyric_html.replace('\t','').replace('\r','').split('\n') #\t,\r 제거하고 \n 기준으로 나누기
        lyric_html = ''.join(lyric_html) # 공백 기준으로 조인

        matched = re.search(r"-->(.*)<br/>", lyric_html)
        lyric = matched.group(1).strip()
        lyric = lyric.replace('<br/>', '\n') # 데이터 전처리 : <br/> 태그를 \n으로 변경

        # 가사 앞뒤 빈칸 제거
        lyric_list = []
        for line in lyric.split('\n'):
            lyric_list.append(line.strip())
        lyric = ('\n').join(lyric_list)
        lyrics.append(lyric)

    except: # 가사가 없으면
        lyric = "없음"
        lyrics.append(lyric)


    # ip 차단 방지용
    sleep(1)


    print(i) # 데이터 수집이 되고 있는지 확인용

print("끝", "\n")
#print(singer_s)
#print(singer_list)
#print(like_counts)

chart_list = { # dict:key, 컬럼명 : 데이터
    'song_id': id_list, #아이디
    'song_name': title_list, #노래제목
    'artist': singer_list, #아티스트
    'like_count': like_counts, #좋아요 수
    'album_name': album_list, #앨범명,
    'genre':genre_list
}

music = pd.DataFrame.from_dict(chart_list, orient='index') # dict 데이터를 데이터 프레임으로 변환
music = music.transpose() # 행과 열 바꾸기

writer = pd.ExcelWriter("2019_charts.xlsx") # 편집자 실행

music.to_excel(writer, sheet_name='2019s chart', startrow=1, header=True)
# 데이터를 엑셀 형식(xlsx)으로 저장, 시작 행 번호, 헤더 존재 설정

writer.close() # 편집자 닫기
