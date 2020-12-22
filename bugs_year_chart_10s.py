import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

#year = [6685,6684,6683,7479,11152,15389,20440,25698,30871,36737] : 2010년대
#year = [6720,6719,6718,6717,6716,6715,6713,6712,6710,6709] # 2000년대
#year = [6800,6799,6798,6796,6795,6794,6793,6792,6791,6790] # 1990년대
#year = [6826,6827,6828,6829,6830,6831,6832,6833,6834,6835] # 1980년대
#year = [6815,6816,6817,6818,6819,6820,6821,6822,6823,6824] # 1970년대
#year = [6804,6808,6809,6810,6811,6812,6813] # 1960년대 - 여기부터 저장명 조금 수정해야 함
year = [6801,6802] # 1940,1950 년대

for i in range(len(year)):
    # 1. url 받아오기
    url = 'https://music.bugs.co.kr/musicpd/albumview/' + str(year[i])
    request = requests.get(url)
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')

    song_list = soup.find("table", class_="list.trackList")

    titles = soup.select('p.title')
    artists = soup.select('p.artist')
    albums = soup.select('td.left > a.album')

    song_title = []
    song_artist = []
    album_list = []
    like_counts = []
    song_lyrics = []
    album_img_url = []


    # 2. url에서 id 부분만 추출하기
    id_url_list = []
    id_list = []

    # 시대별 차트 리스트에서 url만 가져오기
    for elem in soup.find_all('a', href=re.compile('https://music.bugs.co.kr/track')):
        id_url_list.append(elem['href'])

    for j in range(len(id_url_list)):
        a = id_url_list[j].lstrip('https://music.bugs.co.kr/track/')  # 링크1 제거

        a1 = a.rstrip('wl_ref=list_tr_08_mab')  # 링크2 제거
        b = a1.rstrip('?')  # 물음표 제거

        id_list.append(b) # 여기까지 잘 나오는 중

    # 타이틀, 가수, 앨범명
    for k in range(len(id_list)):
        rank = k + 1

        title = titles[k].text.strip().split('\n')[0]
        song_title.append(title)

        artist = artists[k].text.strip().split('\n')[0]
        song_artist.append(artist)

        album = albums[k].text.strip().split('\n')[0]
        album_list.append(album)



    # 좋아요 & 가사 & 앨범 이미지(url)
    for m in range(len(id_list)):
        l_url = 'https://music.bugs.co.kr/track/' + str(id_list[m]) + '?wl_ref=list_tr_08_mab'
        l_request = requests.get(l_url)
        l_html = l_request.text
        l_soup = BeautifulSoup(l_html, "html.parser")

        # 좋아요
        like_count = str(l_soup.select(
            '#container > section.sectionPadding.summaryInfo.summaryTrack > div > div.etcInfo > span > a > span > em'))
        like_count = re.sub('<.+?>', '', like_count, 0)
        like_counts.append(like_count)

        # 가사
        lyric = str(l_soup.select(
            '#container > section.sectionPadding.contents.lyrics > div.innerContainer > div.lyricsContainer > p > xmp'))
        lyric = re.sub('<.+?>', '', lyric, 0)
        song_lyrics.append(lyric)

        # 앨범 이미지
        a_img = l_soup.find("li", class_="big").find("img")
        img_src = a_img.get('src')
        album_img_url.append(img_src)

    print(str(i) + '위')


    #df 생성 후 excel로 저장
    column_list = {
        'song_id': id_list,
        'song_name': song_title,
        'artist': song_artist,
        'album': album_list,
        'Like_Count': like_counts,
        'Lyric': song_lyrics,
        'cover_url': album_img_url
    }

    df = pd.DataFrame.from_dict(column_list, orient='index')
    df = df.transpose()

    writer = pd.ExcelWriter("Bugs_196" + str(i) + ".xlsx")

    df.to_excel(writer, sheet_name= '196'+str(i), startrow=1, header=True)

    writer.close()