import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from systemPart import get_kakaoKey
from systemPart import itemQuery
import models
import picPath

def inventory(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	user_inven = models.Inventory.query.filter_by(user_id=userProfile.id).all()
	answer = ""
	answer += "💰: "+ str("{:,}".format(int(userProfile.gold))) + " Gold\n"
	answer += "💎: "+ str("{:,}".format(int(userProfile.loginPoint))) + " p\n\n"
	
	if not user_inven: # 가방에 아무것도 없을 때
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": answer + "(아무것도 없음)"
		}
		}
		]
		}
		}

	else: # 가방에 아이템 있을 때
		user_equipment = models.db.session.query(models.Inventory,models.ItemBook).filter(models.ItemBook.id == models.Inventory.itemNo, models.ItemBook.category=='장비', models.Inventory.user_id ==userProfile.id).order_by(models.Inventory.name).all()
		if user_equipment:
			answer += "장비 🛡\n——————————————\n"
			
			for inven, itembook in user_equipment:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " 🔒"
				answer += "\n"
		
		user_ingredient = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='재료').order_by(models.Inventory.name).all()
		if user_ingredient:
			answer += "\n재료 🪄\n——————————————\n"
			user_ingredient = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='재료', models.Inventory.value == None).order_by(models.Inventory.name).all()
			for inven, itembook in user_ingredient:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " 🔒"
				answer += "\n"

		fish_list = ["가오리","고등어","꽃게","복어", "상어","성게","연어","오징어","잉어","참치", "해마"]
		for fish in fish_list:
			user_fish = models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name == fish).count()
			if user_fish > 0:
				answer += "- " + fish + "   " + str(user_fish) + "\n"
		
		
		user_odds = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='기타').order_by(models.Inventory.name).all()
		if user_odds:
			answer += "\n기타 🧩\n——————————————\n"
			
			for inven, itembook in user_odds:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " 🔒"
				answer += "\n"
				
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": answer
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "610fc056a5a4854bcb94d908",
		"action": "block",
		"label": "설명보기 📝"
		},
		{
		"blockId": "610e4299defb4e3121f2eb62",
		"action": "block",
		"label": "팔기 💫"
		},
		{
		"blockId": "61137c29b39c74041ad10ec9",
		"action": "block",
		"label": "잠금 🔒"
		}
		]
		}
		}
	
	return res

def fish_inven(reqData): #물고기 인벤토리
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	user_fish = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='재료', models.Inventory.value.like('%cm%')).order_by(models.db.cast(models.Inventory.value, models.db.Float).desc()).all()
			
	if not user_fish: # 물고기 없을 때
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": answer + "(아무것도 없음)"
		}
		}
		]
		}
		}

	else: # 물고기 있을 때
		answer = "\n내 물고기 🐟\n잠금할때 \"물고기명 치수\"\n——————————————\n"
		
		for inven, itembook in user_fish:
			answer += "- " + inven.name + "   " + inven.value
			if inven.lock == 1:
				answer += " 🔒"
			answer += "\n"
		
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": answer
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "61137c29b39c74041ad10ec9",
		"action": "block",
		"label": "잠금 🔒"
		}
		]
		}
		}
	return res
	
def viewItemDescript(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res

	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	req = reqData['action']['detailParams']['select_item']['value']	
	pickItem = models.ItemBook.query.filter_by(itemName=req).first()
	
	if pickItem is None:
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
		"text": "찾는 아이템이 없습니다"
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "610fc056a5a4854bcb94d908",
		"action": "block",
		"label": "다시입력 ✏️"
		},
		
		]
		}
		}
	
	else:
		has_item = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name==pickItem.itemName).first()
		if has_item is None:
			item_name = pickItem.itemName
		else:
			item_name = pickItem.itemName + "  🎒"
			
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"itemCard":{
		"imageTitle": {
		"title": "No. " + str(pickItem.id),
		"description": "도감번호"
		},
		"title": "설명",
		"description": pickItem.descript,
		"profile": {
		"title": item_name,
		"imageUrl": pickItem.itemImg
		
		},
		"itemList": [
		{
		"title": "분류",
		"description": pickItem.category
		},
		{
		"title": "스펙",
		"description": pickItem.spec
		},
		{
		"title": "판매가격",
		"description": str("{:,}".format(int(pickItem.sellPrice))) + " Gold"
		},
		],
		"buttons": [
		{
		"label": "공유하기 🤘",
		"action": "share",
		},
		{
		"label": "다른 아이템 🔎",
		"action": "block",
		"blockId": "610fc056a5a4854bcb94d908"
		},
		],
		}
		}
		]
		}
		}
	
	return res

def sellItem(reqData): # 아이템 판매
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
	req = reqData['action']['detailParams']['sell_info']['value']
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	if '일괄판매' in req: #일괄판매 입력시
		categories = req.split(" ")[0]
		
		if models.ItemBook.query.filter_by(category=categories).first() is None: # category 잘못 입력시
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
			"text": "잘못된 입력정보 입니다"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "610e4299defb4e3121f2eb62",
			"action": "block",
			"label": "다시입력 ✏️"
			},
			
			]
			}
			}
			return res
		
		total_gold = 0
		quantity = 0
		user_items = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.user_id==userProfile.id, models.ItemBook.id == models.Inventory.itemNo, models.ItemBook.category== categories, models.Inventory.lock==0).order_by(models.Inventory.name).all()
		for item, x in user_items:
			total_gold += item.quantity * x.sellPrice
			quantity += item.quantity
		
		res = {
		"version": "2.0",
		"context": {
		"values": [
		{
		"name": "n_sell_info",
		"lifeSpan": 1,
		"params": {
		"pickItem": categories,
		"quantity": total_gold
		}
		},
		]
		},
		"template": {
		"outputs": [
		{
		"itemCard": {
		"description": "위의 정보로 일괄판매를 진행합니다",
		"profile": {
		"title": "판매 정보",
		"imageUrl": picPath.default1319
		},
		"itemList": [
		{
		"title": "아이템",
		"description": categories
		},
		{
		"title": "판매수량",
		"description": str(quantity) + "개"
		},
		{
		"title": "판매가격",
		"description": str("{:,}".format(total_gold)) + " Gold"
		},
		],
		"buttons": [
		{
		"label": "네",
		"action": "block",
		"blockId": "6110e28bb39c74041ad0ff68"
		},
		{
		"label": "아니요",
		"action": "block",
		"blockId": "6110e020401b7e060181e484"
		},
		],
		"buttonLayout" : "horizontal"
		}
		}
		]
		}
		}
		
		return res	
	
	else: # 일반 판매
		quantity = ""
		pickItem = ""
		
		if req[-1] == '개':
			req = req[:-1]
		
		try:
			quantity = req.split(" ")[-1]
			quantity = int(quantity)
		except:
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
			"text": "잘못된 입력정보 입니다"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "610e4299defb4e3121f2eb62",
			"action": "block",
			"label": "다시입력 ✏️"
			},
			
			]
			}
			}
		
		
			
		for itemPuzzle in req[:-1]:
			pickItem += itemPuzzle
			
		pickItem = pickItem[:-len(str(quantity))]
			
		userItem = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name==pickItem, models.Inventory.lock == 0).first()
		
		if userItem is None or userItem.quantity < quantity:
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
			"text": "잘못된 입력정보 입니다"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "610e4299defb4e3121f2eb62",
			"action": "block",
			"label": "다시입력 ✏️"
			},
			
			]
			}
			}
		
		else:
			pickItem_info = models.ItemBook.query.filter_by(itemName=userItem.name).first()
			res = {
			"version": "2.0",
			"context": {
			"values": [
			{
			"name": "n_sell_info",
			"lifeSpan": 1,
			"params": {
			"pickItem": userItem.id,
			"quantity": quantity
			}
			},
			]
			},
			"template": {
			"outputs": [
			{
			"itemCard": {
			"description": "위의 정보로 판매를 진행합니다",
			"profile": {
			"title": "판매 정보",
			"imageUrl": picPath.default1319
			},
			"itemList": [
			{
			"title": "아이템",
			"description": pickItem
			},
			{
			"title": "판매수량",
			"description": str(quantity) + "개"
			},
			{
			"title": "판매가격",
			"description": str("{:,}".format(int(pickItem_info.sellPrice * quantity))) + " Gold"
			},
			],
			"buttons": [
			{
			"label": "네",
			"action": "block",
			"blockId": "6110e28bb39c74041ad0ff68"
			},
			{
			"label": "아니요",
			"action": "block",
			"blockId": "6110e020401b7e060181e484"
			},
			],
			"buttonLayout" : "horizontal"
			}
			}
			]
			}
			}
	
	return res
		

def sellItem_yes(reqData): # 판매 확정
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	pickItem = reqData['contexts'][0]['params']['pickItem']['value']
	quantity = reqData['contexts'][0]['params']['quantity']['value']
	
	if models.ItemBook.query.filter_by(category=pickItem).first() is None: # 일반 판매 확정
		itemQuery.changeAGold(pickItem, userProfile.id, quantity)
		models.db.session.commit()
	
	else: # 일괄판매 확정
		user_items = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.user_id==userProfile.id, models.ItemBook.id == models.Inventory.itemNo, models.ItemBook.category== pickItem, models.Inventory.lock == 0).all()
		for item, x in user_items:
			itemQuery.changeAGold(item.id, userProfile.id, item.quantity)
		models.db.session.commit()
	
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
	"text": "성공적으로 판매하였습니다"
	}
	},
	],
	"quickReplies": [
	{
	"blockId": "610e4299defb4e3121f2eb62",
	"action": "block",
	"label": "팔기 💫"
	},
	{
	"label": "인벤토리 🎒",
	"action": "block",
	"blockId": "6109213f3dcccc79addb1958"
	},
	]
	}
	}

	return res
	
def itemLock(reqData): # 아이템 잠금기능
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
  
	fish_list = ["해마","상어", "연어", "참치","가오리", "복어", "잉어", "고등어","오징어", "꽃게", "성게"]
	req = reqData['action']['detailParams']['lockItem']['value']
	
	pickItem = models.Inventory.query.filter(models.Inventory.name==req, models.Inventory.user_id == userProfile.id).first()
	
	if pickItem is None: # 입력 아이템명이 올바르지 않을때
		for fish in fish_list: #물고기인지 확인
			if fish in req:
				if req[-1] != 'm':
					req += " cm"
				if len(req.split(" ")) != 3:
					req = req[:-2] + " cm"
				print(req)
				pickItem = models.Inventory.query.filter(models.Inventory.name==req.split(" ")[0], models.Inventory.user_id == userProfile.id, models.Inventory.value == (req.split(" ")[1] + " " + req.split(" ")[2])).first()
		if pickItem is None:
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
			"text": "잘못된 입력정보 입니다"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "61137c29b39c74041ad10ec9",
			"action": "block",
			"label": "다시입력 ✏️"
			},
			
			]
			}
			}
			
			return res
			
	
	# 정상 입력 혹은 물고기
	if pickItem.lock == 1:
		pickItem.lock = 0
		answer = pickItem.name + " 해제되었습니다 🔓"
		
	else:
		pickItem.lock = 1
		answer = pickItem.name + " 잠겼습니다 🔒"
		
	models.db.session.commit()
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"simpleText": {
	"text": answer
	}
	}
	],
	"quickReplies": [
	{
	"label": "인벤토리 🎒",
	"action": "block",
	"blockId": "6109213f3dcccc79addb1958"
	},
	{
	"blockId": "61137c29b39c74041ad10ec9",
	"action": "block",
	"label": "잠금 🔒"
	}
	]
	}
	}
	
	return res
		
