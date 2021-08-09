# crawling용 모듈
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests

# 카카오톡 챗봇 영화 제공서비스 실행 함수
def movie_search(search_type, start_cnt): 
    movie_url = { 'rank' : 'https://movie.naver.com/movie/running/current.nhn', # 네이버영화 현재 상영작 예매순위 1~20위
                  'schdule' : 'https://movie.naver.com/movie/running/premovie.nhn?order=reserve' # 네이버영화 개봉 예정작 예매순 1~20위 
                }

    img_url = []        # 포스터 경로 url
    title = []          # 영화 제목
    description = []    # 세부 정보 : 영화 예매 순위 응답 - 평점과 예매율, 개봉 예정작 응답 - 개봉예정일
    link_url = []       # 영화 예매 및 정보가 제공되는 사이트로 연결을 위한 웹 페이지 경로 url
    
    if search_type == 'rank': # 영화 예매 순위 요청
        url = movie_url[search_type]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # soup = soup_rank
        
        img_tag = soup.find_all("div", {"class":"thumb"})   # 영화 포스터 이미지, 제목, 정보제공 링크가 있는 태그
        cnt = 1
        for src in img_tag:
            if cnt >= start_cnt and cnt < start_cnt+5:      # 카트 리스트 응답은 한번에 최대 5개만 가능하므로 정보를 5개만 저장함
                src_img = src.find('img')
                img_url.append(src_img.get('src'))
                title.append(src_img.get('alt'))

                src_link = src.find('a')
                link_url.append('https://movie.naver.com' + src_link.get('href')) # 링크 url 완성
            cnt+=1
        img_url.insert(0,'')            # 카트 리스트로 응답을 보내기 위해서 위해 첫 인덱스에는 제목같은 내용이 들어가므로 각 데이터에 내용 삽입
        title.insert(0,'영화 예매순위') # 카트 리스트 제목
        link_url.insert(0,url)          # 카트 리스트 제목란은 크롤링 페이지로 이동가능하도록 링크 삽입

        get_score = soup.find_all("span",{"class" : "num"}) # 평점과 예매율이 있는 태크
        cnt=1
        temp=''
        for i in get_score:
            if start_cnt == 1:
                if cnt >= 1 and cnt < 11: # 평점, 예매율이 번갈아 가면서 저장되기 때문에 5개의 영화에 대해서 총 10개의 데이터를 받음
                    if cnt % 2 == 1: 
                        temp = i.text
                    else:
                        description.append('평점 : ' + temp + '\t' + '예매율 : ' + i.text + '%') # 세부 정보에 평점과 예매율 저장
            else:
                if cnt >= 11 and cnt < 21: 
                    if cnt % 2 == 1: 
                        temp = i.text
                    else:
                        description.append('평점 : ' + temp + '\t' + '예매율 : ' + i.text + '%')
            cnt+=1
        description.insert(0,'')
        
        button_message = "영화 예매 순위 더보기" # 총 10위까지 응답을 위해서 첫 메시지에는 "순위 더보기 버튼"을 넣어주기 위한 버튼 클릭 시 발화되는 메세지
        
    else:
        url = movie_url[search_type]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # soup = soup_schdule
        
        img_tag = soup.find_all("div", {"class":"thumb"})
        cnt = 1
        for src in img_tag:
            if cnt >= start_cnt and cnt < start_cnt+5:
                src_img = src.find('img')
                img_url.append(src_img.get('src'))
                title.append(src_img.get('alt'))

                src_link = src.find('a')
                link_url.append('https://movie.naver.com' + src_link.get('href'))
            cnt+=1
        img_url.insert(0,'')
        title.insert(0,'개봉예정 영화')
        link_url.insert(0,url)
        
        sch_date = soup.find_all("dl", {'class' : 'info_txt1'})
        cnt=1
        for i in sch_date:
            if cnt >= start_cnt and cnt < start_cnt+5:
                temp = i.text.replace('\t','').replace('\n','').replace('\r','').split(',')
                for text in temp:
                    if '개봉' in text: temp=text
                temp = temp.split('|')[-1].split('감독')[0]
                description.append(temp)
            cnt+=1
        description.insert(0,'')
        
        button_message = "개봉예정 영화 더보기"

    # 응답 메시지가 첫 메시지인지 더보기 요청인지에 따라 첫 메시지일 때만 "더보기" 버튼 생성, 순위 표시    
    if start_cnt == 1: # 첫번째 응답 메시지에 순위와 출처 추가 및 버튼 생성
        title[0] = title[0] + ' (출처: 네이버영화)' 
        button_data = [
                        {
                          "type": "block",
                          "label": "+ 더보기",
                          "message" : button_message, # 버튼 클릭 시 사용자가 전송한 것과 동일하게 하는 메시지
                          "data": {
                            }
                        }
                      ]
    else:
        title[0] = title[0] + ' (출처: 네이버영화)'
        button_data = [
                {
                  "type": "text", # 버튼 타입을 텍스트로 하고 라벨 및 메시지를 비우면 버튼이 나오지 않음(두 번의 메시지를 동일한 포맷으로 res 변수로 만들기 위함)
                  "label": "",
                  "message" : "",
                  "data": {
                    }
                }
              ]
        
        
    listItems=[]

    cnt=0
    for i in range(6): # 응답용 카트 리스트 타입의 res에 추가할 정보 완성
        if cnt == 0: itemtype = 'title' # 카드 이미지의 첫 type은 title
        else: itemtype = 'item'         # 카드 이미지의 제목 다음 type은 item
            
        listItems.append({
                "type": itemtype,               # 카드 리스트의 아이템 티입
                "imageUrl": img_url[i],         # 이미지 링크 url
                "title": title[i],              # 제목
                "description": description[i],  # 세부 정보
                "linkUrl": {
                  "type": "OS",                 # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                    "webUrl": link_url[i]       # 영화 정보 링크 url
                    }
                })
        cnt+=1
        
    return listItems, button_data

def movie(reqData):
    req = reqData
    
    input_text = req['userRequest']['utterance'] # 사용자가 전송한 실제 메시지
    
    if '개봉' in input_text: # 전송 메시지에 "개봉"이 있을 경우는 개봉 예정작 정보를 응답
        search_type = 'schdule'
    else:                   # "개봉"이 메시지에 없으면 예매 순위를 응답
        search_type = 'rank'
        
    if '더보기' in input_text: # 더보기를 요청했을 경우는 메시지에 더보기가 입력되게 설정을 해서 이 경우는 6위부터 10위까지 저장
        start_cnt = 6
    else:
        start_cnt = 1         # 첫 요청일 경우 1위 부터 5위까지 저장

    # 검색 타입(예매 순위 or 개봉 예정작)과 검색 시작 번호를 movie_search 함수로 전달하여 아이템과 버튼 설정을 반환받음  
    listItems, button_data = movie_search(search_type, start_cnt) 

    # 카드 리스트형 응답용 메시지
    res = {
          "contents": [
            {
              "type": "card.list",
              "cards": [
                {
                  "listItems": listItems,
                    "buttons": button_data
                }
              ]
            }
          ]
        }            

    # 전송
    return res
