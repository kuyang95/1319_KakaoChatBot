# crawling용 모듈
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import requests

def corona():
	req = requests.get('http://ncov.mohw.go.kr/')
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
			
	cp = soup.select_one('div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li > span.data')
	outcp = soup.select_one('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li:nth-child(2) > span.data')
			
	answer = '오늘 확진자 수 입니다\n\n국내발생: %s 해외유입: %s'%(cp.text, outcp.text)
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
	
