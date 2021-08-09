# crawling용 모듈
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib
import requests

def weather(reqData):
	req = reqData
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
	
	return res
	
