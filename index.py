from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify, Flask
from flask import current_app as app

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import urllib

import json
 

#main = Blueprint('main', __name__, url_prefix='/')


app = Flask(__name__)


      


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
            title.insert(0,'영화 예매 순위') # 카트 리스트 제목
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
                              if '개봉' in text: 
                                    temp=text
                        temp = temp.split('|')[-1].split('감독')[0]
                        description.append(temp)
                  cnt+=1
            description.insert(0,'')
        
            button_message = "개봉 예정 영화 더보기"

      # 응답 메시지가 첫 메시지인지 더보기 요청인지에 따라 첫 메시지일 때만 "더보기" 버튼 생성, 순위 표시    
      if start_cnt == 1: # 첫번째 응답 메시지에 순위와 출처 추가 및 버튼 생성
            title[0] = title[0] + '(1위~5위)_출처: Naver영화' 
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
            title[0] = title[0] + '(6위~10위)_출처: Naver영화'
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
            if cnt == 0: 
                  itemtype = 'title' # 카드 이미지의 첫 type은 title
            else: 
                  itemtype = 'item'         # 카드 이미지의 제목 다음 type은 item
            
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

@app.route('/')
def index():
      html= "<h1>서버</h1>"
      return html

@app.route('/testwt', methods=['POST'])
def testwt():
      
      req = request.get_json()
    
      params = req['action']['detailParams']
    
      if 'sys_location' not in params.keys(): # 입력 텍스트에 지역이 없을 경우는 바로 경고 메시지 전송
            res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "지역을 입력하세요."
                        }
                    }
                ]
            }
        }

            return jsonify(res)
      if 'sys_location' in params.keys(): # 지역을 시 구 동으로 3개까지 입력을 받을 수 있어서 순서대로 location에 저장
            location = params['sys_location']['value']
      if 'sys_location1' in params.keys():
            location += ' + ' + params['sys_location1']['value']
      if 'sys_location2' in params.keys():
            location += ' + ' + params['sys_location2']['value']
    
      location_encoding = urllib.parse.quote(location + '+날씨') # url 인코딩
      url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%s'%(location_encoding)
    
      req = Request(url)
      page = urlopen(req)
      html = page.read()
      soup = BeautifulSoup(html, 'html.parser')
    
      if soup.find('span', {'class':'btn_select'})==None:    # 동일 시에 구만 다른 같은 이름의 동이 있을 경우 에러발생
            region = soup.find('li', {'role' : 'option'}).text 
      else:
            region = soup.find('span', {'class':'btn_select'}).text
    
      if 'sys_date_period' in params.keys(): # 주 단위의 날씨를 요청했을 경우
            weekly_weather = soup.find_all('li', {'class':'date_info today'})
            answer = '%s 주간 기상정보입니다.\n\n' % (region)
            answer += '요일 날짜 강수확률 기온\n'
            for i in weekly_weather:
                  answer += i.text.replace('     강수확률','').replace('    최저,최고 온도','').replace('  ','/')[0:-1] + '\n'
            
      elif 'sys_date' not in params.keys() or 'today' in params['sys_date']['value']: # 날짜 관련 문구가 없거나 "오늘"을 입력했을 경우
            info = soup.find('p', {'class': 'cast_txt'}).text
            temp_rain_info = soup.find_all('dd', {'class':'weather_item _dotWrapper'})
            temp = temp_rain_info[0].text.replace('도','')
            rain_rate = temp_rain_info[8].text
            sub_info = soup.find_all('dd')
            finedust = sub_info[1].text.replace('㎍/㎥', '㎍/㎥ ')
            Ultrafinedust = sub_info[2].text.replace('㎍/㎥', '㎍/㎥ ')
        
            answer = '%s \n현재 기상정보입니다.\n\n' %(region)
            answer += info + '\n'
            answer += '기온 : ' + temp + '\n'
            answer += '강수확률 : ' + rain_rate + '\n'
            answer += '미세먼지 : ' + finedust + '\n'
            answer += '초미세먼지 : ' + Ultrafinedust
    
      elif 'tomorrow' in params['sys_date']['value']: # 내일 날씨를 요청했을 경우
            def convert(text):
                  text = text.split(' ')
                  return ' '.join(text).split()

            tomorrow = soup.find_all('li', {'class':'date_info today'})[1].text
            tomorrow = convert(tomorrow)

            info = soup.find('div', {'class':'tomorrow_area _mainTabContent'})
            cast = info.find_all('div', {'class':'info_data'})

            answer = '%s \n내일 기상정보입니다.\n\n' %(region)
            answer += '기온 : ' + tomorrow[-1] + '\n'
            answer += '기상 : ' + convert(cast[0].text)[0] + '/' + convert(cast[1].text)[0] + '\n'
            answer += '강수확률 : ' + tomorrow[3] + '/' + tomorrow[5] + '\n'
            answer += '미세먼지 : ' + convert(cast[0].text)[-1] + '/' + convert(cast[1].text)[-1]
        
    # 일반 텍스트형 응답용 메시지
      res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

      return jsonify(res)

## 음악차트

@app.route('/testmusic',methods=['POST'])
def testmusic():
      
      req = request.get_json()
      block_name = req['userRequest']['block']['name']
      
      if block_name == '음악 순위':
             RANK = 10 ## 멜론 차트 순위가 1 ~ 100위까지 있음
 
      header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
      req = requests.get('https://www.melon.com/chart/week/index.htm', headers = header) ## 주간 차트를 크롤링 할 것임
      html = req.text
      parse = BeautifulSoup(html, 'html.parser')
 
      titles = parse.find_all("div", {"class": "ellipsis rank01"}) 
      singers = parse.find_all("div", {"class": "ellipsis rank02"}) 
      albums = parse.find_all("div",{"class": "ellipsis rank03"})
 
      title = []
      singer = []
      album = []
      answer = '음악 주간 차트 TOP 10 입니다.\n\n'
      
      for t in titles:
            title.append(t.find('a').text)
 
      for s in singers:
            singer.append(s.find('span', {"class": "checkEllipsis"}).text)

      for a in albums:
            album.append(a.find('a').text)
 
      for i in range(RANK):
            answer += '%d위:  %s - %s\n'%(i+1, title[i], singer[i])
                  
      res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                  }
                }
            ]
        }
      }

      return jsonify(res)
      
      
@app.route('/testresult', methods=['POST'])
def testresult():
      res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "Hello 1319"
                        }
                  }
                  ]
            }
      }

      return jsonify(res)


@app.route('/movies', methods=['POST']) # 영화 정보 블럭에 스킬로 연결된 경로
def movies():
      req = request.get_json()
      input_text = req['userRequest']['utterance'] # 사용자가 전송한 실제 메시지
    
      if '개봉' in input_text: # 전송 메시지에 "개봉"이 있을 경우는 개봉 예정작 정보를 응답
            search_type = 'schdule'
      else:                 # "개봉"이 메시지에 없으면 예매 순위를 응답
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
      return jsonify(res)

@app.route('/corona', methods=['POST'])
def corona():
      req = request.get_json()
      input_text = req['userRequest']['utterance']
      
      if '코로나' in input_text:
            req = requests.get('http://ncov.mohw.go.kr/')
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            
            cp = soup.select_one('div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li > span.data')
            outcp = soup.select_one('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li:nth-child(2) > span.data')
            
            answer = '오늘 확진자 수 입니다.\n\n국내발생: %s 해외유입: %s'%(cp.text, outcp.text)
            
     
      res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }
        
    # 전송
      return jsonify(res)
      
if __name__ =="__main__":
      app.run(debug=True,host="0.0.0.0", port=1234)


      
      

