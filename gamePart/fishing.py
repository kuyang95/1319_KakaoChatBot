import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
from systemPart import itemQuery
from systemPart import loginSession


ᅣfish_list = {"legend":["해마","상어"], "epic":["연어", "참치","가오리"], "uncommon":["복어", "잉어", "고등어" ], "common":["오징어", "꽃게", "성게"]}
sizing = {"해마": "50 90", "상어": "40 100", "연어": "40 70", "참치": "40 70","가오리": "50 80", "복어": "20 40", "잉어": "20 55", "고등어": "20 50", "오징어": "0 20", "꽃게": "0 10", "성게": "0 5"}
waiting_ment = ["세월을 낚자 💦", "커피 맛이 좋군 ☕️", "바람이 기분좋게 분다 🌬", "햇살이 수면을 핥... ✨", "너무 바쁘게 사는거 아닌가 🚛", "잠시 쉬어가게.. 🏖", "상어를 낚을테다 🤸‍♀️", "이런곳에선 클래식이지 🎧", "저녁은 뭐먹지 💭"]

def fishing(reqData):
	if loginSession.loginSession(reqData) is not True:
		return loginSession.res
	else:
		login_context = loginSession.loginContext(reqData)
		userProfile = models.User.query.filter_by(userid = reqData['contexts'][0]['params']['user_id']['value']).first()
	
	
	
	pail = []
	status = 0
	chance = 3
	casting = random.randrange(1,11)
	isCatch = 0
	
	if len(reqData['context']) > 1:
		pail = reqData['context'][1]['pail']['value']
		status = reqData['context'][1]['status']['value']
		chance = reqData['context'][1]['chance']['value']
		casting = reqData['context'][1]['casting']['value']
		isCatch = reqData['context'][1]['isCatch']['value']
	
	if status < 2 and casting > 7 and chance > 0 and isCatch == 0: # 잡지 않은 상태이고 캐스팅 성공
		res = {
		"version": "2.0",
		"context": {
		"values": [
		login_context,
		],
		{
		"name": "p_pail_list",
		"lifeSpan": 2,
		"params": {
		  "pail": pail,
		  "status": 1
		  "chance" : (chance -1)
		  "casting" : casting
		  "isCatch": random.randrange(1,3)
		}
		}
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": "입질중 🐟"
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "약하게 친다 💫️"
		},
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "강하게 친다 💥"
		}
		]
		}
		}
		
		
	elif status==0 and casting <= 6: # 캐스팅 실패
		res = {
		"version": "2.0",
		"context": {
		"values": [
		login_context,
		],
		{
		"name": "p_pail_list",
		"lifeSpan": 2,
		"params": {
		  "pail": pail,
		  "status": 0
		  "chance" : chance
		  "casting" : random.randrange(1,11)
		  "isCatch": 0
		}
		}
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": waiting_ment
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "기다리기 🌱️"
		},
		]
		}
		}
	
	elif chance == 0 and isCatch == 0: # 3번 찬스 다써서 물고기 놓침
		res = {
		"version": "2.0",
		"context": {
		"values": [
		login_context,
		],
		{
		"name": "p_pail_list",
		"lifeSpan": 2,
		"params": {
		  "pail": pail,
		  "status": 0
		  "chance" : 3
		  "casting" : random.randrange(1,11)
		  "isCatch": 0
		}
		}
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": "앗, 물고기가 도망갔다❗️"
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "낚시 🎣️"
		},
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "돌아가기 🏠️"
		},
		]
		}
		}
	
	elif isCatch == 1: #물고기 잡음
		pickFish = randrange(1,201)
		size = 0
		
		# 확률 50 30 19.5 0.5
		if pickFish <= 100:
			pickFish = random.choice(fish_list["common"])
			size = round(random.uniform(sizing[pickFish].split(" ")[0], sizing[pickFish].split(" ")[1]), 2)
		
		elif pickFish <= 160:
			pickFish = random.choice(fish_list["uncommon"])
			size = round(random.uniform(sizing[pickFish].split(" ")[0], sizing[pickFish].split(" ")[1]), 2)
		
		elif pickFish <= 199:
			pickFish = random.choice(fish_list["epic"])
			size = round(random.uniform(sizing[pickFish].split(" ")[0], sizing[pickFish].split(" ")[1]), 2)
		
		else:
			pickFish = random.choice(fish_list["legend"])
			size = round(random.uniform(sizing[pickFish].split(" ")[0], sizing[pickFish].split(" ")[1]), 2)
		
		models.db.session.add(models.Inventory(pickFish, userProfile.id, models.ItemBook.query.filter_by(itemName=pickFish).first().id)
		models.db.session.commit()
		getFish = models.db.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name == pickFish).order_by(models.Inventory.id.desc()).limit(1).first()
		getFish.spec = str(size) + " cm"
		models.db.session.commit()
		
		res = {
		"version": "2.0",
		"context": {
		"values": [
		login_context,
		],
		{
		"name": "p_pail_list",
		"lifeSpan": 2,
		"params": {
		  "pail": pail,
		  "status": 0
		  "chance" : 3
		  "casting" : random.randrange(1,11)
		  "isCatch": 0
		}
		}
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": "앗, 물고기가 도망갔다❗️"
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "낚시 🎣️"
		},
		{
		"blockId": "6111481f401b7e060181e789",
		"action": "block",
		"label": "돌아가기 🏠️"
		},
		]
		}
		}
