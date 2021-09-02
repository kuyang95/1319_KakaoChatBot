import sys
import os
import random
import datetime


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
from systemPart import itemQuery
from systemPart import get_kakaoKey


def growing(reqData):
	systemCheck = get_kakaoKey.get_kakaoKey(reqData)
	if systemCheck != 0:
		if systemCheck == 1:
			return get_kakaoKey.res
		elif systemCheck == 2:
			return get_kakaoKey.notice(reqData)
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	user_growing = models.GrowingPet.query.filter_by(user_id=userProfile.id).order_by(models.GrowingPet.level.desc()).all()
	userSt = models.UserStatus.query.filter_by(id = userProfile.id).first()
	growing_list = []
	counter = "  "
	req = reqData['userRequest']['utterance']
	
	if req == '훈련센터로 이동 🥬' or req == '훈련센터' or req == '이동'  or req.split(" ")[0] == '훈련센터': # 훈련센터 인덱스로 이동문구
		for pet in user_growing:
			if pet.status == "수업중..🏫": # 시간 계산해서 쉬는중으로 바꿔줌
				current_time = datetime.datetime.now()
				old_time = datetime.datetime.strptime(pet.timer, "%Y-%m-%d %H:%M:%S.%f") # str 을 datetime 형태로 바꿔줌
				time_flows = current_time - old_time
				
				if time_flows.days *86400  + time_flows.seconds > 20400: # 학교 끝
					pet.status = "휴식중..🏖"
					pet.academic += 1
					models.db.session.commit()
					
				else:
					remaining_time = 14400 - time_flows.seconds
					hours = remaining_time // 3600
					s = remaining_time - hours*3600
					mu = s // 60
					ss = s - mu*60
					remaining_time = '\'' +  str(hours) +  '시간 ' + str(mu) +  '분 ' + str(ss) +  '초\'  남음'
					pet_status = pet.status + "  " + remaining_time
			
			else:
				pet_status = pet.status
					
			pet_info = models.PetBook.query.filter_by(name=pet.name).first()
			growing_list.append({       
			"title": pet_status,
			"profile": {
			"title": pet_info.name,
			"imageUrl": pet_info.img	
			},
			"itemList": [
			{
			"title": "레벨",
			"description": pet.level
			},
			{
			"title": "성격",
			"description": pet.personality
			},
			],
			"buttons": [
			{
			"label": "키우기" + counter,
			"action": "block",
			"blockId": "61235128401b7e0601822e38"
			}
			],
			}
			)
			counter += "  "
		
		
				
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"carousel": {
		"type": "itemCard",
		"items": growing_list
		}
		}
		]
		}
		}
			
		return res
		
	elif req[0:3] == '키우기' or req.split(" ")[0] == '뒤로': # 키우기 눌렀을 때
		if req[0:3] == '키우기':
			select_pet = int((len(req)-5)/2)
			userSt.growing_select = user_growing[select_pet].id
			models.db.session.commit()
			
		ren_ment = []
		ren_ment.append(['음냥냥, 골을 넣는 꿈을 꿨어', '달리기 좋아.\n하루종일 초원에서 달리기시합 하고싶다', '앞 산에가면 동물들이 점령하고 지키고있대.\n진짜야?', '세상에 내 이름을 알리고싶어'])
		ren_ment.append(['포기는 배추 셀때나 쓰는 말이라고','뭐든지 끝날때까지 열심히 해야한댔어', '마지막 에너지를 쏟아부을 때,\n그때가 진짜야', '요즘은 눕기만하면 바로 잠이 쏟아져'])
		ren_ment.append(['무서울땐 내 뒤에 숨어.\n내가 앞잘설게', '신뢰는 한결같은 모습에서 나온대. 나는 어때?', '심장이 빨리 뛸 때 살아있는게 느껴져서 좋아', '짜증날땐 맛있는걸 먹자.\n그만한게 없지'])
		ren_ment.append(['바다에서 낚시를 하면 해마가 잡힌다던데 알아?', '분명 나는 사람이였던 것 같은데..', '바깥세상에는 뭐가 있을까 너무 궁금해', '나는 밥먹을 때 양손을 다 써서 먹어.\n짱이지?'])
		ren_ment.append(['이것도 좋고, 저것도 좋아.\n다좋아!','나는 못하는게 없지.\n한똑똑 한다구','혼자있으면 나는 몽상가가 돼.\n약간 미래에 대한 거랄까?', '주인이랑 있을때가 제일 좋아!'])
		ment = []
		
		
		pet = models.GrowingPet.query.filter_by(id = userSt.growing_select).first()
		pet_info = models.PetBook.query.filter_by(name=pet.name).first()
		
		buttons = []
		buttons.append({
		"blockId": "61235128401b7e0601822e38",
		"action": "block",
		"label": "상태보기 📝️"
		})
		
		if pet.status == "수업중..🏫":
			current_time = datetime.datetime.now()
			old_time = datetime.datetime.strptime(pet.timer, "%Y-%m-%d %H:%M:%S.%f") # str 을 datetime 형태로 바꿔줌
			time_flows = current_time - old_time	
	
			remaining_time = 14400 - time_flows.seconds
			hours = remaining_time // 3600
			s = remaining_time - hours*3600
			mu = s // 60
			ss = s - mu*60
			remaining_time = '\'' +  str(hours) +  '시간 ' + str(mu) +  '분 ' + str(ss) +  '초\'  남음'
			ment.append(pet.status + "  " + remaining_time)
			
			
		else: # 휴식중
			if pet.personality == '강인한':
				ment = ren_ment[0]
			elif pet.personality == '끈기있는':
				ment = ren_ment[1]
			elif pet.personality == '듬직한':
				ment = ren_ment[2]
			elif pet.personality == '창의적인':
				ment = ren_ment[3]
			elif pet.personality == '다재다능한':
				ment = ren_ment[4]
			
			if pet.level < 10:
				buttons.append({
				"blockId": "61275bd04738391855a634af",
				"action": "block",
				"label": "먹이주기 🐟"
				})
			if pet.intimacy < 100:
				buttons.append({
				"blockId": "612f47b67bccb93a7b6f0498",
				"action": "block",
				"label": "놀기 🥁"
				})
			if pet.academic < 2:
				buttons.append({
				"blockId": "61235128401b7e0601822e38",
				"action": "block",
				"label": "교육보내기 🏫"
				})
			
		answer = "레벨 — " + str(pet.level) +"\n친밀도 — " + str(pet.intimacy) + "\n소양교육 — "
		if pet.academic == 0:
			answer += "이수안함"
		elif pet.academic == 1:
			answer += "교육중"
		else:
			answer += "완료"

		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		 {
		"simpleText": {
		"text": answer
		} 
		},
		{
		"simpleImage": {
		"imageUrl": pet_info.img
		}
		},
		 {
		"simpleText": {
		"text":  random.choice(ment) + " 💬"
		} 
		},
		],
		"quickReplies": buttons
		
		}
		}
		
		return res
	
	elif req.split(" ")[0] == '상태보기':
		pet = models.GrowingPet.query.filter_by(id = userSt.growing_select).first()
		pet_info = models.PetBook.query.filter_by(name=pet.name).first()
		
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"itemCard": {
		"imageTitle": {
		"title": pet.status,
		},
		"profile": {
		"title": pet_info.name,
		"imageUrl": pet_info.img	
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
		"title": "성격",
		"description": pet.personality
		},
		{
		"title": "교육",
		"description": pet.academic
		},
		{
		"title": "친밀도",
		"description": pet.intimacy
		},
		{
		"title": "레벨",
		"description": pet.level
		},
		{
		"title": "힘",
		"description": pet.strength
		},
		{
		"title": "지능",
		"description": pet.intellect
		},
		{
		"title": "체력",
		"description": pet.health
		},
		{
		"title": "방어력",
		"description": pet.shild
		},
		],
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "61235128401b7e0601822e38",
		"action": "block",
		"label": "아이템사용 🧶️"
		},
		{
		"blockId": "61235128401b7e0601822e38",
		"action": "block",
		"label": "놓아주기 🍃"
		},
		{
		"blockId": "61235128401b7e0601822e38",
		"action": "block",
		"label": "뒤로 👈️"
		},
		
		]
		}
		}
		return res
	
	elif req.split(" ")[0] == '아이템사용' or req[0:2] == '사용':
		if req.split(" ")[0] == '아이템사용':
			item_list = []
			personality_change = models.Inventory.query.filter(models.Inventory.name == '강형욱 특별지도권', models.Inventory.user_id == userProfile.id).first()
			if personality_change is not None:
				personality_change_info = models.ItemBook.query.filter_by(itemName = '강형욱 특별지도권').first()
				item_list.append({       
				"profile": {
				"title": personality_change.name,
				"imageUrl": personality_change_info.itemImg
				},
				"itemList": [
				{
				"title": "효과",
				"description": "성격변경"
				},
				],
				"buttons": [
				{
				"label": "사용" + " ",
				"action": "block",
				"blockId": "61235128401b7e0601822e38"
				}
				],
				}
				)
			
			pet_toy = models.Inventory.query.filter(models.Inventory.name == '펫장난감', models.Inventory.user_id == userProfile.id).first()
			if pet_toy is not None:
				pet_toy_info = models.ItemBook.query.filter_by(itemName = '펫장난감').first()
				item_list.append({       
				"profile": {
				"title": pet_toy.name,
				"imageUrl": pet_toy_info.itemImg
				},
				"itemList": [
				{
				"title": "효과",
				"description": "친밀도 상승"
				},
				],
				"buttons": [
				{
				"label": "사용" + "  ",
				"action": "block",
				"blockId": "61235128401b7e0601822e38"
				}
				],
				}
				)
				
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			 {
			"simpleText": {
			"text": "사용하실 아이템을 선택해주세요 🧶"
			} 
			},
			{
			"carousel": {
			"type": "itemCard",
			"items": item_list
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "뒤로 👈️"
			},
			]
			}
			}
				
			return res
		
		else:
			pet = models.GrowingPet.query.filter_by(id=userSt.growing_select).first()
			if len(req) == 3: # 성격변화권 사용함
				personality_list = ['강인한', '듬직한', '창의적인', '끈기있는', '다재다능한']
				old_personality = pet.personality
				filteredList = list(filter(lambda x: x!=old_personality, personality_list)) 
				new_personality = random.choice(filteredList)
				
				pet.personality = new_personality
				itemQuery.deleteA("강형욱 특별지도권", userProfile.id, 1)
				models.db.session.commit()
				
				answer = "\"" +  pet.name + "\"" + " 의 성격이 변했다❗️\n" + old_personality + " ⇾ " + new_personality
				
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				 {
				"simpleText": {
				"text": answer
				} 
				},
				],
				"quickReplies": [
				{
				"blockId": "61235128401b7e0601822e38",
				"action": "block",
				"label": "상태보기 📝️"
				},
				]
				}
				}
					
				return res
			elif len(req) == 4: # 펫장난감 사용함
				number = randrange(20,36)
				pet.intimacy += number
				if pet.intimacy > 100:
					pet.intimacy = 100
				models.db.session.commit()
				
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				 {
				"simpleText": {
				"text": pet.name + "의 친밀도가 " + str(number) + " 상승했습니다❗️"
				} 
				},
				],
				"quickReplies": [
				{
				"blockId": "61235128401b7e0601822e38",
				"action": "block",
				"label": "상태보기 📝️"
				},
				]
				}
				}
				
			
	elif req.split(" ")[0] == '놓아주기' or req == '확인':
		print("come")
		pet = models.GrowingPet.query.filter_by(id = userSt.growing_select).first()
		pet_info = models.PetBook.query.filter_by(name=pet.name).first()
		if req.split(" ")[0] == '놓아주기':
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"itemCard": {
			"profile": {
			"title": pet_info.name,
			"imageUrl": pet_info.img	
			},
			"title": "정말로 보내시겠습니까?",
			"description": "되돌릴 수 없습니다",
			"itemList": [
			{
			"title": "레벨",
			"description": pet.level
			},
			],
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "확인"
			},
			{
			"blockId": "6110e020401b7e060181e484",
			"action": "block",
			"label": "아니요"
			},
			]
			}
			}
			return res
		else:
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": "\"" + "잘가 " + pet.name + "❕" + "\""
			}
			}
			],
			"quickReplies": [
			{
		    "label": "훈련센터 🥬",
		    "action": "block",
		    "blockId": "61235128401b7e0601822e38"
		    }
			]
			}
			}
				
			models.db.session.delete(pet)
			models.db.session.commit()
			return res
	
	elif req.split(" ")[0] == '교육보내기' or req == '보내기':
		pet = models.GrowingPet.query.filter_by(id = userSt.growing_select).first()
		
		if req.split(" ")[0] == '교육보내기':
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": pet.name + "을(를) 학교에 보내겠습니까❔"
			}
			}
			],
			"quickReplies": [
			{
		    "label": "보내기",
		    "action": "block",
		    "blockId": "61235128401b7e0601822e38"
		    },
		    {
		    "label": "아니요",
		    "action": "block",
		    "blockId": "6110e020401b7e060181e484"
		    }
			]
			}
			}
			
			return res
		
		else: # 학교 보내기 확정
			pet = models.GrowingPet.query.filter_by(id = userSt.growing_select).first()
			pet.timer = datetime.datetime.now()
			pet.status = "수업중..🏫"
			
	
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": "ฅ(๑˙o˙๑)ฅ \n학교 다녀오겠습니다❕"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "뒤로 👈️"
			}
			]
			}
			}
			
			return res
	
				
