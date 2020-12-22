import re
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from pandas import DataFrame
import pandas as pd


# 2012년대 노래 시대별 차트
# https://www.melon.com/chart/age/list.htm?idx=1&chartType=YE&chartGenre=KPOP&chartDate=2012&moved=Y
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

age_url = "https://www.melon.com/chart/age/list.htm"

params = { # 여기서 chartDate만 유동적으로 바꿀 수 있게 코드 수정하기
    'idx':'1',
    'chartType':'YE',    #YEAR
    'chartGenre':'KPOP',
    'chartDate':'2012',
    'moved':'Y',
}

response = requests.get(age_url, params=params, headers=headers)
soup = bs(response.text, 'html.parser')
song_list = soup.select('.lst50, .lst100')

id_list = []     #고유 아이디 리스트
title_list = []  #노래제목 리스트
genre_list = []  #장르 리스트
date_list = []   #발매일 리스트
album_list = []  #앨범 리스트
singer_list = [] #가수 리스트
lyrics = []      #가사 리스트
like_counts = [] #좋아요 수

for i, meta in enumerate(song_list, 1):
    # 순위, 제목
    rank = i
    try:
        title = meta.select('a[href*=playSong]')[0].text
    except:
        title = meta.select('.wrap_song_info .ellipsis')[0].text

    title = title.strip()
    title_list.append(title)

    # print('\n')
    # print(str(params['chartDate'])+'년')
    # print(str(rank)+ '위.', title)


    # 노래 데이터 url의 html 추출
    song_id_html = str(meta.select('a[onclick*=SongDetail]'))
    matched = re.search(r"\'(\d+)\'", song_id_html)
    song_id = matched.group(1)
    id_list.append(song_id) #고유id 리스트 데이터 추가


    front_url = 'https://www.melon.com/song/detail.htm?songId='
    song_url = front_url + song_id


    # 가수, 앨범명, 발매날짜, 장르
    response = requests.get(song_url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    singer_html = soup.select('.wrap_info .artist a')

    # 가수
    singer_s = []
    if len(singer_html) != 0:
        for html in singer_html:
            singer_s.append(html['title'])
        singer_list.append(singer_s)

    else:
        # url 없는 various artists용
        singer_html = str(soup.select('.wrap_info .artist')[0])
        singer_html = singer_html.replace('\t','').replace('\r','').split('\n')
        singer_html = ''.join(singer_html)
        matched = re.search(r">(.*)<", singer_html)
        singer_s.append(matched.group(1))
        singer_list.append(singer_s)

    # 가수가 여러 명일 때 하나의 string으로 표현
    singer_s = ', '.join(singer_s)
    #singer_list.append(singer_s)


    #앨범명
    album_name_html = str(soup.select('.list dd')[0])
    matched = re.search(r">(.*)<", album_name_html)
    matched2 = re.search(r">(.*)<", matched.group(1))
    album_name = matched2.group(1).strip()
    album_list.append(album_name)

    #좋아요 수
    #like_count_html = str(soup.select('//*[@id="lst50"]/td[5]/div/button/span[2]/text()')) # 결과 X
    #like_count_html = str(soup.select('span#d_like_count'))       #총건수
    # like_count_html = str(soup.select('span#d_like_count.cnt'))n  #총건수
    # like_count_html = str(soup.select('#downloadfrm > div > div > div.entry > '
    #                                   'div.button.d_song_like span.cnt')) #총건수
    #like_count_html = str(soup.select('#btnLike > span.cnt')) # 얘도 총건수
    like_count_html = str(soup.select('#btnLike > span#d_like_count'))
    matched = re.search(r">(.*)<", like_count_html)
    like_count = matched.group(1)
    like_counts.append(like_count)

    #발매날짜
    song_date_html = str(soup.select('.list dd')[1])
    matched = re.search(r">(.*)<", song_date_html)
    song_date = matched.group(1)
    date_list.append(song_date)

    #장르
    song_genre_html = str(soup.select('.list dd')[2])
    matched = re.search(r">(.*)<", song_genre_html)
    song_genre = matched.group(1)
    genre_list.append(song_genre)


    # 가사가 있으면 추출j
    try:
        lyric_html = str(soup.select('.section_lyric .wrap_lyric .lyric')[0])
        lyric_html = lyric_html.replace('\t','').replace('\r','').split('\n')
        lyric_html = ''.join(lyric_html)

        matched = re.search(r"-->(.*)<br/>", lyric_html)
        lyric = matched.group(1).strip()
        lyric = lyric.replace('<br/>', '\n')

        # 가사 앞뒤 빈칸 제거
        lyric_list = []
        for line in lyric.split('\n'):
            lyric_list.append(line.strip())
        lyric = ('\n').join(lyric_list)
        lyrics.append(lyric)

    except:
        lyric = "없음"
        lyrics.append(lyric)


    # ip 차단 방지용
    sleep(1)


    print(i)

print("끝", "\n")
#print(singer_s)
#print(singer_list)
#print(like_counts)

chart_list = {
    'song_id': id_list, #아이디
    'song_name': title_list, #노래제목
    'artist': singer_list, #아티스트
    'like_count': like_counts, #좋아요 수
    'album_name': album_list, #앨범명,
    'genre':genre_list
}

music = pd.DataFrame.from_dict(chart_list, orient='index')
music = music.transpose()

writer = pd.ExcelWriter("2019_charts.xlsx")

music.to_excel(writer, sheet_name='2019s chart', startrow=1, header=True)

writer.close()
