# crawling용 모듈
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import requests

def musicChart():
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
	
	return res
	
