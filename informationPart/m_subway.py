from flask import Flask, request, jsonify
# crawling용 모듈
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import urllib
import json

def m_subway():
	req = request.get_json()
	subway_name = req['action']['detailParams']
	subway_name = subway_name['subway_name']['value']
	subway_name = quote(subway_name[:-1])
	
	if subway_name is not None:
		requestUrl = urllib.request.urlopen("http://swopenapi.seoul.go.kr/api/subway/624551574e6b7579313037676e4e7742/json/realtimeStationArrival/0/5/" + subway_name).read().decode('utf8')
		resJson = requestUrl
		resJson = json.loads(resJson)
		runStatus = resJson["errorMessage"]["code"]
	
		if runStatus == "INFO-200":
			res = {
				"version": "2.0",
				"template": {
				"outputs": [
						{
							"simpleText": {
								"text": "운행중인 열차가 없어요."
							}
						}
					]
				}
			}
		
		elif runStatus == "INFO-000":
			answer = resJson['barvlDt']
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
	
	
	
