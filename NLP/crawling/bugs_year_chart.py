import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 벅스 뮤직에서 음악 데이터 가져오기 - 좋아요 포함

# year 변수는 연도별 차트의 고유 아이디임. 패턴을 찾기 힘들어 일일이 확인하면서 데이터를 가져옴
#year = [6685,6684,6683,7479,11152,15389,20440,25698,30871,36737] : 2010년대
#year = [6720,6719,6718,6717,6716,6715,6713,6712,6710,6709] # 2000년대
#year = [6800,6799,6798,6796,6795,6794,6793,6792,6791,6790] # 1990년대
#year = [6826,6827,6828,6829,6830,6831,6832,6833,6834,6835] # 1980년대
#year = [6815,6816,6817,6818,6819,6820,6821,6822,6823,6824] # 1970년대
year = [6804,6808,6809,6810,6811,6812,6813] # 1960년대 - 여기부터 저장명 조금 수정해야 함

for i in range(len(year)):
    # 1. url 받아오기
    url = 'https://music.bugs.co.kr/musicpd/albumview/' + str(year[i]) # full url 생성
    request = requests.get(url) # url 불러오기 요청
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
    id_url_list = [] # 노래 고유 번호가 있는 href 데이터를 담는 리스트
    id_list = [] # 노래 고유 번호를 담는 리스트

    # 시대별 차트 리스트에서 url만 가져오기
    for elem in soup.find_all('a', href=re.compile('https://music.bugs.co.kr/track')): # 해당 url에서 a 태그를 전부 찾기
        id_url_list.append(elem['href']) # a 태그 중에서 href 데이터만 따로 빼내서 id_url_list에 담기

    for j in range(len(id_url_list)):
        a = id_url_list[j].lstrip('https://music.bugs.co.kr/track/')  # 링크1 제거
        # lstrip() : 데이터의 왼쪽에서 괄호 안 데이터의 패턴이 발견되면 제거

        a1 = a.rstrip('wl_ref=list_tr_08_mab')  # 링크2 제거
        # rstrip() : 데이터의 오른쪽에서 괄호 안 데이터의 패턴이 발견되면 제거
        b = a1.rstrip('?')  # 물음표 제거

        id_list.append(b) # 여기까지 잘 나오는 중

    # 타이틀, 가수, 앨범명
    for k in range(len(id_list)):
        rank = k + 1 # k=0부터 시작

        title = titles[k].text.strip().split('\n')[0] # titles 데이터에서 양쪽 공백을 제거하고, \n을 기준으로 분리
        song_title.append(title) #song_title에 추가

        artist = artists[k].text.strip().split('\n')[0] # artists 데이터에서 양쪽 공백을 제거하고, \n을 기준으로 분리
        song_artist.append(artist) #song_artist에 추가

        album = albums[k].text.strip().split('\n')[0] # albums 데이터에서 양쪽 공백을 제거하고, \n을 기준으로 분리
        album_list.append(album) #album_list에 추가



    # 좋아요 & 가사 & 앨범 이미지(url)
    for m in range(len(id_list)):
        l_url = 'https://music.bugs.co.kr/track/' + str(id_list[m]) + '?wl_ref=list_tr_08_mab' # 전체 url 생성 : 곡 상세 페이지
        l_request = requests.get(l_url)
        l_html = l_request.text
        l_soup = BeautifulSoup(l_html, "html.parser")

        # 좋아요
        like_count = str(l_soup.select(
            '#container > section.sectionPadding.summaryInfo.summaryTrack > div > div.etcInfo > span > a > span > em')) # 좋아요 데이터가 있는 html 구조
        like_count = re.sub('<.+?>', '', like_count, 0) # 특수문자 제거
        like_counts.append(like_count) # 리스트에 추가

        # 가사
        lyric = str(l_soup.select(
            '#container > section.sectionPadding.contents.lyrics > div.innerContainer > div.lyricsContainer > p > xmp')) # 가사 데이터가 있는 html 구조
        lyric = re.sub('<.+?>', '', lyric, 0)
        song_lyrics.append(lyric)

        # 앨범 이미지
        a_img = l_soup.find("li", class_="big").find("img") # li 태그의 class가 big인 곳에서, img 태그를 가진 것 찾기
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

    df = pd.DataFrame.from_dict(column_list, orient='index') # dict를 dataframe 형식으로 변환
    df = df.transpose() # 행과 열 전환

    writer = pd.ExcelWriter("Bugs_196" + str(i) + ".xlsx") # 편집자 실행

    df.to_excel(writer, sheet_name= '196'+str(i), startrow=1, header=True) # 엑셀로 저장

    writer.close() # 편집자 종료