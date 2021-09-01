from . import myPage
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from systemPart import get_kakaoKey
from systemPart import itemQuery
import models
import picPath

def shop():
		
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"carousel": {
	"type": "basicCard",
	"items": [
	{
	"title": "장비 상점",
	"description": "장비 사는데 돈쓰면 고기는 누가 사?",
	"thumbnail": {
	
	"imageUrl": picPath.equipment_shop,
	},
	"buttons": [
	{
	"action": "block",
	"label": "이동",
	"blockId": "610bd074b39c74041ad0eef6"
	},
	]
	},
	{
	"title": "펫 상점",
	"description": "Love Animal, Love Nature",
	"thumbnail": {
	"imageUrl": picPath.pet_shop
	},
	"buttons": [
	{
	"action": "block",
	"label": "이동",
	"blockId": "611279c8401b7e060181f081"
	},
	]
	},
	
	]
	}
	}
	]   
	}
	}

	return res


def buyAnEquipment(reqData):
	systemCheck = get_kakaoKey.get_kakaoKey(reqData)
	if systemCheck != 0:
		if systemCheck == 1:
			return get_kakaoKey.res
		elif systemCheck == 2:
			return get_kakaoKey.notice(reqData)
			
	item_list = ['검 0강', '알', '강형욱 특별지도권', '펫장난감']
	req = reqData['userRequest']['user']['id']
	userProfile = models.User.query.filter_by(kakaoKey=req).first()
	
	req = item_list[len(reqData['userRequest']['utterance']) -3]
	
	if req == '검 0강':
		user_sword = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name.like('%검%'), models.Inventory.name.like('%강%')).count()		
		if user_sword >= 3:
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{"simpleImage": {
			"imageUrl": picPath.system_ment,
			}
			},
			{
			"simpleText": {
			"text": "장비는 3개까지 보유 가능합니다"
			}
			}
			]
			}
			}
			return res

		
	
	pickItem = models.ItemBook.query.filter_by(itemName = req).first()
	if userProfile.gold < pickItem.buyPrice: # 돈 부족
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleImage": {
		"imageUrl": picPath.system_ment,
		}
		},{
		"simpleText": {
		"text": "골드가 부족합니다"
		}
		}
		],
		 "quickReplies": [
		{
		"label": "활동하러 가기 🏃‍♂️",
		"action": "block",
		"blockId": "610caea93dcccc79addb2654"
		}
		]
		}
		}
		return res

	itemQuery.addA(pickItem.itemName,userProfile.id, 1)
	userProfile.gold -= pickItem.buyPrice
	models.db.session.commit()
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"simpleText": {
	"text": "성공적으로 구입했습니다"
	}
	}
	],
	"quickReplies": [
	{
	"label": "인벤토리 🎒",
	"action": "block",
	"blockId": "6109213f3dcccc79addb1958"
	}
	]
	}
	}

	return res
	
def shop_equipment(): # 장비 상점
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"carousel": {
	"type": "itemCard",
	"items": [
	{       
	"title": "평범해 보이지만..",
	"description": "강화를 통해 성장할 수 있는 검이다",
	"profile": {
	"title": "검",
	"imageUrl": picPath.sword
	
	},
	"itemList": [
	{
	"title": "공격력",
	"description": "1"
	
	},
	{
	"title": "구매비용",
	"description":  "300 Gold"
	},
	],
	"buttons": [
	{
	"label": "구입" + " ",
	"action": "block",
	"blockId": "610bd39a199a8173c6c47eba"
	}
	],
	},
	{       
	"title": "준비중..",
	"description": "준비중..",
	"profile": {
	"title": "준비중..",
	"imageUrl": picPath.sword
	
	},
	"itemList": [
	{
	"title": "준비중..",
	"description": "준비중.."
	
	},
	{
	"title": "구매비용",
	"description":  "0 Gold"
	},
	],
	"buttons": [
	{
	"label": "구입",
	"action": "block",
	"blockId": "610bcb6a401b7e060181d207"
	}
	],
	}
	]
	}
	}
	]
	}
	}
		
	return res

def shop_pet(): # 펫 상점
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"carousel": {
	"type": "itemCard",
	"items": [
	{       
	"title": "다리 밑에서 주워온 알",
	"description": "이것은 단순한 알이 아니다",
	"profile": {
	"title": "알",
	"imageUrl": picPath.egg
	
	},
	"itemList": [
	{
	"title": "생김새",
	"description": "작고 귀여움"
	
	},
	{
	"title": "구매비용",
	"description":  "100,000 Gold"
	},
	],
	"buttons": [
	{
	"label": "구입" + "  ",
	"action": "block",
	"blockId": "610bd39a199a8173c6c47eba"
	}
	],
	},
	{       
	"title": "펫 훈련계의 거장에게 받는 트레이닝",
	"description": "진짜 성격을 찾게될지도..!",
	"profile": {
	"title": "강형욱 특별지도권",
	"imageUrl": picPath.change_personality
	
	},
	"itemList": [
	{
	"title": "효과",
	"description": "성격 변경"
	
	},
	{
	"title": "구매비용",
	"description":  "200,000 Gold"
	},
	],
	"buttons": [
	{
	"label": "구입   ",
	"action": "block",
	"blockId": "610bd39a199a8173c6c47eba"
	}
	],
	},
	{       
	"title": "펫과 친해지세요",
	"description": "펫 용품은 원래 비싸요",
	"profile": {
	"title": "펫장난감",
	"imageUrl": picPath.pet_toy
	
	},
	"itemList": [
	{
	"title": "효과",
	"description": "친밀도 상승"
	
	},
	{
	"title": "구매비용",
	"description":  "300,000 Gold"
	},
	],
	"buttons": [
	{
	"label": "구입" + "    ",
	"action": "block",
	"blockId": "610bd39a199a8173c6c47eba"
	}
	],
	},
	
	
	]
	}
	}
	]
	}
	}
		
	return res
	
