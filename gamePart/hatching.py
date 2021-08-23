import sys
import os
import random
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import picPath
import models
from systemPart import itemQuery
from systemPart import get_kakaoKey

egg_list = {"legend":["냥카르트"], "epic":["나무정령", "벚꽃정령", "콘콘", "돌돌이", "롱롱이"], "uncommon":["머쉬룸", "물댕댕","비틀즈", "베리프", "스타핀", "스타핌", "황금박쥐", "그리림"], "common":["불뱀","나붕이", "부스", "불닭", "블루밍", "찍찍이"]}
personality_list = ['강인한', '듬직한', '창의적인', '끈기있는', '다재다능한']
def hatching(reqData): # 부화소 입력 시
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
	
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	userSt = models.UserStatus.query.filter_by(id=userProfile.id).first()
	req = reqData['userRequest']['utterance']
	print(req)
	if req == '사용하기': # 부화 하려고 시도
		user_egg = models.db.session.query(models.Inventory, models.ItemBook).filter(models.ItemBook.id == models.Inventory.itemNo, models.ItemBook.id ==42, models.Inventory.user_id == userProfile.id).all()
		
		if not user_egg: # 보유 알이 없을 때
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleImage": {
			"imageUrl": picPath.system_ment,
			}
			},
			{
			"simpleText": {
			"text": "부화 가능한 알이 없어요"
			} 
			}
			],
			"quickReplies": [
			{
			"label": "상점으로 이동 🛒",
			"action": "block",
			"blockId": "6109219c25cb590ace33a6cf"
			
			}
			]
			}
			}
			return res
		elif user_egg and userSt.isHatching == 0: # 보유 알이 있을 때
			eggs = []
			for egg, x in user_egg: eggs.append({"label": egg.name, "action": "block", "blockId": "611e502b199a8173c6c4c993" })
			
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": "부화할 알을 선택하세요 ⏳"
			}
			}
			],
			"quickReplies": eggs
			}
			}
		
			return res

	elif req == '받아오기' and userSt.isHatching == 2: # 훈련센터로 이동
		user_growing = models.GrowingPet.query.filter_by(user_id = userProfile.id).count()
		pet_info = models.PetBook.query.filter_by(name = userSt.hatching_pet).first()
		egg_info = models.ItemBook.query.filter_by(itemName = userSt.hatching_egg).first()
		print(user_growing)
		if user_growing > 4: # 최대 5마리까지 한번에 훈련가능이라 넘으면 안됨
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			 {
		    "simpleImage": {
			"imageUrl": picPath.system_ment
		    }
		    },
			{
			"simpleText": {
			"text": "훈련센터가 꽉찼어요"
			}
			}
			],
			"quickReplies": [
			{
		    "label": "훈련센터로 이동 🥬",
		    "action": "block",
		    "blockId": "61235128401b7e0601822e38"
		    }
			]
			}
			}
			return res
		else:
			models.db.session.add(models.GrowingPet(pet_info.name, userSt.pet_personality, pet_info.strength, pet_info.intellect, pet_info.health, pet_info.shild, userProfile.id))
			userSt.isHatching = 0
			models.db.session.commit()
			
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": "훈련센터로 들어갔어요"
			}
			},
			{
			"itemCard":{
			"title": "휴식중..🏖",
			"profile": {
			"title": pet_info.name,
			"imageUrl": pet_info.img
			
			},
			"itemList": [
			{
			"title": "레벨",
			"description": 1
			},
			{
			"title": "성격",
			"description": userSt.pet_personality
			},
			],
			}
			},
			],
			"quickReplies": [
			{
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "훈련센터로 이동 🥬"
			}
			]
			}
			}
			return res
			
			
		
		
	elif req == '확인하기'or userSt.isHatching == 2: # 부화끝나고 펫 확인
		pet_info = models.PetBook.query.filter_by(name = userSt.hatching_pet).first()
		egg_info = models.ItemBook.query.filter_by(itemName = userSt.hatching_egg).first()
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"basicCard": {
		"thumbnail": {
		"imageUrl": pet_info.img,
		"fixedRatio": True,
		"width" : 400,
		"height" : 400
		},
		}
		},
	    {
	     "itemCard": {
		  "imageTitle": {
		  "title": "축하합니다 🎉",
		  "description": "알에서 " + userSt.pet_personality + " " + pet_info.name + " (이)가 태어났어요",
		  },
		  "title": "설명",
		  "description": pet_info.descript,
		  "itemList": [
		  {
		  "title": "속성",
		  "description": pet_info.element
		  },
		  {
		  "title": "타입",
		  "description": pet_info.p_type
		  },
		  {
		  "title": "힘",
		  "description": pet_info.strength
		  },
		  {
		  "title": "지능",
		  "description": pet_info.intellect
		  },
		  {
		  "title": "체력",
		  "description": pet_info.health
		  },
		  {
		  "title": "방어력",
		  "description": pet_info.shild
		  },
		  ],
		  "buttons": [
		  {
		  "label": "받아오기",
		  "action": "block",
		  "blockId": "611e502b199a8173c6c4c993"
		  }
		  ],
		  }
		  }
	    ],
	    }
	    }
		return res
	
	    
	else: # 부화 인덱스 페이지
		if '알' in req: # 알 놓았을 때 쿼리문
			user_egg = models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name == req).first()
			itemQuery.deleteA(user_egg.name, userProfile.id, 1)
			userSt.isHatching = 1
			userSt.hatching_egg = req
			userSt.hatchingTimer = datetime.datetime.now()
			
			if userSt.hatching_egg == '알':
				pet_list = egg_list
			
			# 확률 40 32 25 3
			pick = random.randrange(1,101)
			if pick <= 40:
				pick = random.choice(pet_list["common"])
			elif pick <= 72:
				pick = random.choice(pet_list["uncommon"])
			elif pick <= 97:
				pick = random.choice(pet_list["epic"])	
			else:
				pick = random.choice(pet_list["legend"])
			
			userSt.hatching_pet = pick
			userSt.pet_personality = random.choice(personality_list)
			models.db.session.commit()
			
		if userSt.isHatching == 1: #부화 진행중일때
			current_time = datetime.datetime.now()
			old_time = datetime.datetime.strptime(userSt.hatchingTimer, "%Y-%m-%d %H:%M:%S.%f") # str 을 datetime 형태로 바꿔줌
			time_flows = current_time - old_time
			
			egg_info = models.ItemBook.query.filter_by(itemName = userSt.hatching_egg).first()
			if time_flows.days *86400  + time_flows.seconds > 14400: # 부화 완료
				userSt.isHatching = 2
				models.db.session.commit()
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				{
				"itemCard":{
				"title": "알이 깨어났어요❗️",
				"description": "누가 기다리고 있는지 확인해 보세요",
				"profile": {
				"title": egg_info.itemName,
				"imageUrl": egg_info.itemImg
				
				},
				"itemList": [
				
				{
				"title": "상태",
				"description": "부화완료"
				},
				],
				"buttons":[
				{
				"blockId": "611e502b199a8173c6c4c993",
				"action": "block",
				"label": "확인하기️"
				}
				]
				}
				},
				],
				}
				}

				return res
				
			else: # 부화 진행중
				remaining_time = 14400 - time_flows.seconds
				hours = remaining_time // 3600
				s = remaining_time - hours*3600
				mu = s // 60
				ss = s - mu*60
				remaining_time = "부화까지 " + '\'' +  str(hours) +  '시간 ' + str(mu) +  '분 ' + str(ss) +  '초\'  남았습니다'
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				
				{
				"itemCard":{
				"title": remaining_time,
				"profile": {
				"title": egg_info.itemName,
				"imageUrl": egg_info.itemImg	
				},
				"itemList": [	
				{
				"title": "상태",
				"description": "부화중"
				},
				],
				}
				},
				],
				}
				}

				return res
				
		else: # 부화중인게 없을 때
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"basicCard": {
			"title": "부화기 ❣️",
			"description": "알을 부화시켜 보세요",
			"thumbnail": {
			"imageUrl": picPath.hatching_machine
			},
			"buttons": [
			{
			  "action": "block",
			  "label": "사용하기",
			  "blockId": "611e502b199a8173c6c4c993"
			}
			]
			}
			}
			]
			}
			}
			return res
	
		
	
