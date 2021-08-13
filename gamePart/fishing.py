import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
from systemPart import itemQuery
from systemPart import get_kakaoKey


fish_list = {"legend":["해마","상어"], "epic":["연어", "참치","가오리"], "uncommon":["복어", "잉어", "고등어" ], "common":["오징어", "꽃게", "성게"]}
sizing = {"해마": "50 90", "상어": "40 100", "연어": "40 70", "참치": "40 70","가오리": "50 80", "복어": "20 40", "잉어": "20 55", "고등어": "20 50", "오징어": "5 15", "꽃게": "0 10", "성게": "0 5"}
waiting_ment = ["세월을 낚자 💦", "커피 맛있네 ☕️", "바람이 기분좋게 분다 🌬", "햇살이 수면을 핥... ✨", "여유를 가져보자 🧘", "잠시 쉬어가게.. 🏖", "상어를 낚아보자 🤸‍♀️", "낚시엔 역시 클래식이지 🎧", "저녁은 뭐먹지.. 🍱"]
ren_ment = ["으차.. 으차차 💢", "밀당은 이렇게 호이호이 🪄", "힘이 제법 센걸 💥"]

def fishing(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	pail = "양동이 🪣\n\n"
	status = 0
	casting = random.randrange(1,11)
	isCatch = 0
	
	if len(reqData['contexts']) > 0:
		pail = reqData['contexts'][0]['params']['pail']['value']
		status = int(reqData['contexts'][0]['params']['status']['value'])
		casting = int(reqData['contexts'][0]['params']['casting']['value'])
		isCatch = int(reqData['contexts'][0]['params']['isCatch']['value'])
	
	if status < 2 and casting > 7 and isCatch == 0 or isCatch == 3: # 잡지 않은 상태이고 캐스팅 성공
		text_message = []
		if status ==0:
			text_message.append({
			"simpleImage": {
		"imageUrl": "http://210.111.183.149:1234/static/itemResource/fishing/fish_come.png"
		}})
		
		
		text_message.append({
		"simpleText": {
		"text": "입질중.. 🐟"
		}
		})
		
		
		res = {
		"version": "2.0",
		"context": {
		"values": [
		{
		"name": "p_pail_list",
		"lifeSpan": 1,
		"params": {
		  "pail": pail,
		  "status": 1,
		  "casting" : casting,
		  "isCatch": random.randrange(1,5)
		}
		}
		]
		},
		"template": {
		"outputs": text_message,
		
		"quickReplies": [
		{
		"blockId": "6114dacdb39c74041ad11797",
		"action": "block",
		"label": "약하게 친다 💫️"
		},
		{
		"blockId": "6114dacdb39c74041ad11797",
		"action": "block",
		"label": "강하게 친다 💥"
		}
		]	
		}
		}
		
	
	elif status==0 and casting <= 7: # 캐스팅 실패
		res = {
		"version": "2.0",
		"context": {
		"values": [
		{
		"name": "p_pail_list",
		"lifeSpan": 1,
		"params": {
		  "pail": pail,
		  "status": 0,
		  "casting" : random.randrange(1,11),
		  "isCatch": 0
		}
		}
		]
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": random.choice(waiting_ment)
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "6114dacdb39c74041ad11797",
		"action": "block",
		"label": "기다리기 💭"
		}
		]
		}
		}
		return res
	
	elif isCatch == 4: # 물고기 도망감
		res = {
		"version": "2.0",
		"context": {
		"values": [
		{
		"name": "p_pail_list",
		"lifeSpan": 1,
		"params": {
		  "pail": pail,
		  "status": 0,
		  "casting" : random.randrange(1,11),
		  "isCatch": 0
		}
		}
		],
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": random.choice(ren_ment)
		}
		},
		{
		"simpleText": {
		"text": "앗, 물고기가 도망갔다 💨️"
		}
		},
		],
		"quickReplies": [
		{
		"blockId": "610b602b401b7e060181cdc7",
		"action": "block",
		"label": "돌아가기 🏠️️"
		},
		{
		"blockId": "6114dacdb39c74041ad11797",
		"action": "block",
		"label": "낚시 🎣"
		},
		]
		}
		}
		
	
	elif isCatch == 1 or isCatch == 2: #물고기 잡음
		pickFish = random.randrange(1,201)
		size = 0
		
		# 확률 50 30 19.5 0.5
		if pickFish <= 100:
			pickFish = random.choice(fish_list["common"])
			size = round(random.uniform(int(sizing[pickFish].split(" ")[0]), int(sizing[pickFish].split(" ")[1])), 2)
		
		elif pickFish <= 173:
			pickFish = random.choice(fish_list["uncommon"])
		elif pickFish <= 199:
			pickFish = random.choice(fish_list["epic"])	
		else:
			pickFish = random.choice(fish_list["legend"])
		
		size = round(random.uniform(int(sizing[pickFish].split(" ")[0]), int(sizing[pickFish].split(" ")[1])), 3)
		models.db.session.add(models.Inventory(pickFish, userProfile.id, models.ItemBook.query.filter_by(itemName=pickFish).first().id))
		models.db.session.commit()
		getFish = models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name == pickFish).order_by(models.Inventory.id.desc()).limit(1).first()
		getFish.value = str(size) + " cm"
		models.db.session.commit()
		
		fish_info = models.ItemBook.query.filter_by(itemName=getFish.name).first()
		
		pail += "- " + pickFish + "  " + str(size) + " cm\n" 
		
		res = {
		"version": "2.0",
		"context": {
		"values": [
		{
		"name": "p_pail_list",
		"lifeSpan": 1,
		"params": {
		"pail": pail,
		"status": 0,
		"casting" : random.randrange(1,11),
		"isCatch": 0
		}
		}
		],
		},
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": random.choice(ren_ment)
		}
		},
		{
		"itemCard":{
		"title": ("신난다. " + pickFish + "를 잡았다❗️"),
		"profile": {
		"title": fish_info.itemName,
		"imageUrl": fish_info.itemImg
		
		},
		"itemList": [
		
		{
		"title": "크기",
		"description": getFish.value
		},
		],
		}
		},
		{
		"simpleText": {
		"text": pail
		}
		},
		
		],
		"quickReplies": [
		{
		"blockId": "610b602b401b7e060181cdc7",
		"action": "block",
		"label": "돌아가기 🏠️"
		},
		{
		"blockId": "6114dacdb39c74041ad11797",
		"action": "block",
		"label": "️낚시 🎣"
		},
		]
		}
		}

	return res
