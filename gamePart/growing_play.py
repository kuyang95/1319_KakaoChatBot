import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
import datetime
from sqlalchemy import or_
from systemPart import itemQuery
from systemPart import get_kakaoKey


def growing_play(reqData):
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	userSt = models.UserStatus.query.filter_by(id = userProfile.id).first()
	user_growing = models.GrowingPet.query.filter_by(id=userSt.growing_select).first()
	req = reqData['userRequest']['utterance'].split(" ")[0]
	
	if req == '놀기': # 놀기 인덱스
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": '무엇을 하며 놀까요?'
		} 
		}],
		"quickReplies": [
		{
		"label": "가위바위보 💥",
		"action": "block",
		"blockId": "612f47b67bccb93a7b6f0498"
		},
		{
		"label": "숨바꼭질 😻",
		"action": "block",
		"blockId": "612f47b67bccb93a7b6f0498"
		}
		
		]
		}
		}
		
		return res
		
	elif req in ['가위바위보', '가위', '바위', '보', '다시하기']: # 가위바위보 게임 시작
		com_choice = ['가위', '바위', '보']
		user_choice = ['바위','보','가위']
		emogi = {'가위': '✌️', '바위': '🤛', '보': '✋'}
		
		ren_ment = ['이(가) 무엇을 낼지 고민중이다..💭', '은(는) 무엇을 낼지 정했다 🌝', '이(가) 당신에게 심리전을 걸고있다 🌀']
		if req in ['가위바위보', '다시하기']:
			answer = user_growing.name + random.choice(ren_ment)
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": answer
			} 
			}],
			"quickReplies": [
			{
			"label": "가위 ✌️",
			"action": "block",
			"blockId": "612f47b67bccb93a7b6f0498"
			},
			{
			"label": "바위 🤛",
			"action": "block",
			"blockId": "612f47b67bccb93a7b6f0498"
			},
			{
			"label": "보 ✋",
			"action": "block",
			"blockId": "612f47b67bccb93a7b6f0498"
			},
			
			]
			}
			}
			
			return res
			
		
		else: # 유저가 가위바위보중 하나를 냄
			com = random.choice(com_choice)
			
			if com == req: # 비김
				answer = emogi[req] + " : " + emogi[com]+ "\n비겼다. 다시 가위바위보 💥"
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				{
				"simpleText": {
				"text": answer
				} 
				}],
				"quickReplies": [
				{
				"label": "가위 ✌️",
				"action": "block",
				"blockId": "612f47b67bccb93a7b6f0498"
				},
				{
				"label": "바위 🤛",
				"action": "block",
				"blockId": "612f47b67bccb93a7b6f0498"
				},
				{
				"label": "보 ✋",
				"action": "block",
				"blockId": "612f47b67bccb93a7b6f0498"
				},
				
				]
				}
				}
				
				return res
				
			else: # 유저가 이기거나 지거나
				if com_choice.index(com) == user_choice.index(req):
					user_growing.intimacy += 10
					models.db.session.commit()
					answer = emogi[req] + " : " + emogi[com] + "\n이겼다. 친밀도 10 상승❗️"
				
				else: 
					answer = emogi[req] + " : " + emogi[com] + "\n졌다. 다음엔 이길거야 💦"
					
				buttons = []
				if user_growing.intimacy < 100:
					buttons.append({
					"label": "다시하기 💥",
					"action": "block",
					"blockId": "612f47b67bccb93a7b6f0498"
					})
				
				buttons.append({
				"blockId": "61235128401b7e0601822e38",
				"action": "block",
				"label": "뒤로 👈️"
				})
				
				
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				{
				"simpleText": {
				"text": answer
				} 
				}],
				"quickReplies": buttons
				}
				}
				
				return res
				
	elif req in ['숨바꼭질', '다시찾기', '여기']:
		ren_ment = ['저는 어디에 숨었을까요 🍃', '여기 숨어있으면 모를꺼야 🌝','저 멀리 도망가서 숨어야지 🐾']
		if req in ['숨바꼭질', '다시찾기']:
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": random.choice(ren_ment)
			} 
			},
			{
			"carousel": {
			"type": "basicCard",
			"items": [
			{
			"thumbnail": {
			"imageUrl": picPath.hideandseek
			},
			"buttons": [
			{
			"action": "block",
			"label": "여기 !?",
			"blockId": "612f47b67bccb93a7b6f0498"
			},
			]
			},
			{
			"thumbnail": {
			"imageUrl": picPath.hideandseek
			},
			"buttons": [
			{
			"action": "block",
			"label": "여기 !?",
			"blockId": "612f47b67bccb93a7b6f0498"
			},
			]
			},
			{
			"thumbnail": {
			"imageUrl": picPath.hideandseek
			},
			"buttons": [
			{
			"action": "block",
			"label": "여기 !?",
			"blockId": "612f47b67bccb93a7b6f0498"
			},
			]
			},
			]
			}
			}
			],
			"quickReplies": [{
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "뒤로 👈️"
			}]
			}
			}
			return res
		
		else:
			correct = random.randrange(1,4)
			
			if correct == 1:
				user_growing.intimacy += 10
				models.db.session.commit()
				answer = user_growing.name + " 찾았다 하하하❗️\n친밀도 10 상승"
				
			else:
				answer = "여기 없는것 같다 💦"
				
			buttons = []
			if user_growing.intimacy < 100:
				buttons.append({
				"label": "다시찾기 😻",
				"action": "block",
				"blockId": "612f47b67bccb93a7b6f0498"
				})
			
			buttons.append({
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "뒤로 👈️"
			})
			
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": answer
			} 
			}],
			"quickReplies": buttons
			}
			}
			
			return res
	
