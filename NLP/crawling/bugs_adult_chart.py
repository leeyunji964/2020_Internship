import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 벅스 성인차트 데이터 가져오기 - 전체적으로 연도별 차트와 코드 유사

year = [1970,1980,1990,2000,2010]

for i in range(len(year)):
    # 1. url 받아오기
    url = 'https://music.bugs.co.kr/genre/kpop/adultkpop/trot' + str(year[i]) + '?tabtype=7' # 이 부분은 직접 url을 봐야 함
    request = requests.get(url)
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')

    song_list = soup.find("table", class_="list.trackList") # 해당 연도의 곡 리스트
    # 해당 url에서 class가 list trackList인 'table' 태그의 데이터를 song_list에 담음

    titles = soup.select('p.title') # p 태그의 클래스가 title인 데이터
    artists = soup.select('p.artist') # p 태그의 클래스가 artist인 데이터
    albums = soup.select('td.left > a.album') # td 태그의 클래스가 left이고, 하위 데이터 중 a 태그의 클래스가 album인 데이터

    song_title = [] # 노래 제목
    song_artist = [] # 가수명
    album_list = [] # 앨범명
    like_counts = [] # 좋아요 수
    song_lyrics = [] # 가사
    album_img_url = [] # 앨범 이미지 url


    # 2. url에서 id 부분만 추출하기
    id_url_list = []# 노래의 고유 번호가 있는 href 데이터를 담는 리스트
    id_list = [] # 노래 고유 번호를 담는 리스트

    # 시대별 차트 리스트에서 url만 가져와서 해당 곡의 고유 id 추출해내기
    for elem in soup.find_all('a', href=re.compile('https://music.bugs.co.kr/track')): # 해당 url에서 a 태그를 전부 찾기
        id_url_list.append(elem['href']) # a 태그 중에서 href 데이터만 따로 빼내서 id_url_list에 담기

    for j in range(len(id_url_list)):
        a = id_url_list[j].lstrip('https://music.bugs.co.kr/track/')  # 링크1 제거
        # lstrip() : 데이터의 왼쪽에서 괄호 안 데이터의 패턴이 발견되면 제거

        a1 = a.rstrip('wl_ref=list_tr_08')  # 링크2 제거
        # rstrip() : 데이터의 오른쪽에서 괄호 안 데이터의 패턴이 발견되면 제거
        b = a1.rstrip('?')  # 물음표 제거

        id_list.append(b)

    # 타이틀, 가수, 앨범명
    for k in range(len(id_list)):
        rank = k + 1

        title = titles[k].text.strip().split('\n')[0]
        # titles 데이터에서 양쪽 공백을 제거하고, \n을 기준으로 분리
        song_title.append(title)

        artist = artists[k].text.strip().split('\n')[0]
        # artists 데이터에서 양쪽 공백을 제거하고, \n을 기준으로 분리
        song_artist.append(artist)

        album = albums[k].text.strip().split('\n')[0]
        # albums 데이터에서 양쪽 공백을 제거하고, \n을 기준으로 분리
        album_list.append(album)



    # 좋아요 & 가사 & 앨범 이미지(url)
    for m in range(len(id_list)):
        l_url = 'https://music.bugs.co.kr/track/' + str(id_list[m]) + '?wl_ref=list_tr_08'
        l_request = requests.get(l_url)
        l_html = l_request.text
        l_soup = BeautifulSoup(l_html, "html.parser")

        # 좋아요
        like_count = str(l_soup.select('#container > section.sectionPadding.summaryInfo.summaryTrack > div > div.etcInfo > span > a > span > em'))
        like_count = re.sub('[\<\[].*?[\>\]]', '', like_count, 0) # '[\<\[].*?[\>\]]' # 특수문자 제거
        like_count = like_count.replace(']','')
        like_counts.append(like_count) # 리스트에 추가

        # 가사
        lyric = str(l_soup.select('#container > section.sectionPadding.contents.lyrics > div.innerContainer > div.lyricsContainer > p > xmp'))
        lyric = re.sub('[\<\[].*?[\>\]]', '', lyric, 0) # <.+?>
        lyric = lyric.replace(']','')
        song_lyrics.append(lyric)

        # 앨범 이미지
        a_img = l_soup.find("li", class_="big").find("img")
        img_src = a_img.get('src') # img 태그에서 src 데이터를 img_src에 담음
        album_img_url.append(img_src) # 리스트에 추가

    print(str(i) + '위') # 현재 수집되고 있는지 rank만 출력


    #df 생성 후 excel로 저장
    column_list = { # dict-key
        'song_id': id_list,
        'song_name': song_title,
        'artist': song_artist,
        'album': album_list,
        'Like_Count': like_counts,
        'Lyric': song_lyrics,
        'cover_url': album_img_url
    }

    df = pd.DataFrame.from_dict(column_list, orient='index')
    df = df.transpose() # 행과 열 전환

    writer = pd.ExcelWriter("Bugs_Adult_Chart" + str(i+1) + ".xlsx") # 편집자 실행

    df.to_excel(writer, sheet_name= 'Adult_Chart_'+str(i+1)+'s', startrow=1, header=True)

    writer.close() # 편집자 종료