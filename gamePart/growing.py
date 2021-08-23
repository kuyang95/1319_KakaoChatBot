import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
from systemPart import itemQuery
from systemPart import get_kakaoKey


def growing(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	user_growing = models.GrowingPet.query.filter_by(user_id=userProfile.id).order_by(models.GrowingPet.level).all()
	growing_list = []
	counter = "  "
	req = reqData['userRequest']['utterance']
	
	if req == '훈련센터로 이동 🥬' or req == '훈련센터' or req == '이동':	 # 훈련센터 인덱스로 이동문구
		for pet in user_growing:
			pet_info = models.PetBook.query.filter_by(name=pet.name).first()
			growing_list.append({       
			"title": pet.status,
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
		
	else: # 키우기 눌렀을 때
		select_pet = int((len(req)-5)/2)
		pet = user_growing[select_pet]
		pet_info = models.PetBook.query.filter_by(name=pet.name).first()
		
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleImage": {
		"imageUrl": pet_info.img
		}
		}
		],
		}
		}
		
		return res
	
	
