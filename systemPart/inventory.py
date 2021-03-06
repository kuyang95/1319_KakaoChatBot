import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from systemPart import get_kakaoKey
from systemPart import itemQuery
import models
import picPath

def inventory(reqData):
	systemCheck = get_kakaoKey.get_kakaoKey(reqData)
	if systemCheck != 0:
		if systemCheck == 1:
			return get_kakaoKey.res
		elif systemCheck == 2:
			return get_kakaoKey.notice(reqData)
	
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	user_inven = models.Inventory.query.filter_by(user_id=userProfile.id).all()
	answer = ""
	answer += "π°: "+ str("{:,}".format(int(userProfile.gold))) + " Gold\n"
	answer += "π: "+ str("{:,}".format(int(userProfile.loginPoint))) + " p\n\n"
	
	if not user_inven: # κ°λ°©μ μλ¬΄κ²λ μμ λ
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": answer + "(μλ¬΄κ²λ μμ)"
		}
		}
		]
		}
		}

	else: # κ°λ°©μ μμ΄ν μμ λ
		user_equipment = models.db.session.query(models.Inventory,models.ItemBook).filter(models.ItemBook.id == models.Inventory.itemNo, models.ItemBook.category=='μ₯λΉ', models.Inventory.user_id ==userProfile.id).order_by(models.Inventory.name).all()
		if user_equipment:
			answer += "μ₯λΉ π‘\nββββββββββββββ\n"
			
			for inven, itembook in user_equipment:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " π"
				answer += "\n"
		
		user_ingredient = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='μ¬λ£').order_by(models.Inventory.name).all()
		if user_ingredient:
			answer += "\nμ¬λ£ πͺ\nββββββββββββββ\n"
			user_ingredient = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='μ¬λ£', models.Inventory.value == None).order_by(models.Inventory.name).all()
			for inven, itembook in user_ingredient:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " π"
				answer += "\n"

		fish_list = ["κ°μ€λ¦¬","κ³ λ±μ΄","κ½κ²","λ³΅μ΄", "μμ΄","μ±κ²","μ°μ΄","μ€μ§μ΄","μμ΄","μ°ΈμΉ", "ν΄λ§"]
		for fish in fish_list:
			user_fish = models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name == fish).count()
			if user_fish > 0:
				answer += "- " + fish + "   " + str(user_fish) + "\n"
		
		user_use = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='μ¬μ©').order_by(models.Inventory.name).all()
		if user_use:
			answer += "\nμ¬μ© π\nββββββββββββββ\n"
			
			for inven, itembook in user_use:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " π"
				answer += "\n"
				
		user_odds = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='κΈ°ν').order_by(models.Inventory.name).all()
		if user_odds:
			answer += "\nκΈ°ν π§©\nββββββββββββββ\n"
			
			for inven, itembook in user_odds:
				answer += "- " + inven.name + "   " + str(inven.quantity)
				if inven.lock == 1:
					answer += " π"
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
		"label": "μ€λͺλ³΄κΈ° π"
		},
		{
		"blockId": "610e4299defb4e3121f2eb62",
		"action": "block",
		"label": "νκΈ° π«"
		},
		{
		"blockId": "61137c29b39c74041ad10ec9",
		"action": "block",
		"label": "μ κΈ π"
		}
		]
		}
		}
	
	return res

def fish_inven(reqData): #λ¬Όκ³ κΈ° μΈλ²€ν λ¦¬
	systemCheck = get_kakaoKey.get_kakaoKey(reqData)
	if systemCheck != 0:
		if systemCheck == 1:
			return get_kakaoKey.res
		elif systemCheck == 2:
			return get_kakaoKey.notice(reqData)
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	user_fish = models.db.session.query(models.Inventory, models.ItemBook).filter(models.Inventory.itemNo==models.ItemBook.id, models.Inventory.user_id==userProfile.id, models.ItemBook.category=='μ¬λ£', models.Inventory.value.like('%cm%')).order_by(models.db.cast(models.Inventory.value, models.db.Float).desc()).all()
			
	if not user_fish: # λ¬Όκ³ κΈ° μμ λ
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": answer + "(μλ¬΄κ²λ μμ)"
		}
		}
		]
		}
		}

	else: # λ¬Όκ³ κΈ° μμ λ
		answer = "\nλ΄ λ¬Όκ³ κΈ° π\nμ κΈν λ \"λ¬Όκ³ κΈ°λͺ μΉμ\"\nββββββββββββββ\n"
		
		for inven, itembook in user_fish:
			answer += "- " + inven.name + "   " + inven.value
			if inven.lock == 1:
				answer += " π"
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
		"label": "μ κΈ π"
		}
		]
		}
		}
	return res
	
def viewItemDescript(reqData):
	systemCheck = get_kakaoKey.get_kakaoKey(reqData)
	if systemCheck != 0:
		if systemCheck == 1:
			return get_kakaoKey.res
		elif systemCheck == 2:
			return get_kakaoKey.notice(reqData)
			
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
		"text": "μ°Ύλ μμ΄νμ΄ μμ΅λλ€"
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "610fc056a5a4854bcb94d908",
		"action": "block",
		"label": "λ€μμλ ₯ βοΈ"
		},
		
		]
		}
		}
	
	else:
		has_item = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name==pickItem.itemName).first()
		if has_item is None:
			item_name = pickItem.itemName
		else:
			item_name = pickItem.itemName + "  π"
			
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"itemCard":{
		"imageTitle": {
		"title": "No. " + str(pickItem.id),
		"description": "λκ°λ²νΈ"
		},
		"title": "μ€λͺ",
		"description": pickItem.descript,
		"profile": {
		"title": item_name,
		"imageUrl": pickItem.itemImg
		
		},
		"itemList": [
		{
		"title": "λΆλ₯",
		"description": pickItem.category
		},
		{
		"title": "μ€ν",
		"description": pickItem.spec
		},
		{
		"title": "νλ§€κ°κ²©",
		"description": str("{:,}".format(int(pickItem.sellPrice))) + " Gold"
		},
		],
		"buttons": [
		{
		"label": "κ³΅μ νκΈ° π€",
		"action": "share",
		},
		{
		"label": "λ€λ₯Έ μμ΄ν π",
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

def sellItem(reqData): # μμ΄ν νλ§€
	req = reqData['action']['detailParams']['sell_info']['value']
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	if 'μΌκ΄νλ§€' in req: #μΌκ΄νλ§€ μλ ₯μ
		categories = req.split(" ")[0]
		
		if models.ItemBook.query.filter_by(category=categories).first() is None: # category μλͺ» μλ ₯μ
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
			"text": "μλͺ»λ μλ ₯μ λ³΄ μλλ€"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "610e4299defb4e3121f2eb62",
			"action": "block",
			"label": "λ€μμλ ₯ βοΈ"
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
		"description": "μμ μ λ³΄λ‘ μΌκ΄νλ§€λ₯Ό μ§νν©λλ€",
		"profile": {
		"title": "νλ§€ μ λ³΄",
		"imageUrl": picPath.default1319
		},
		"itemList": [
		{
		"title": "μμ΄ν",
		"description": categories
		},
		{
		"title": "νλ§€μλ",
		"description": str(quantity) + "κ°"
		},
		{
		"title": "νλ§€κ°κ²©",
		"description": str("{:,}".format(total_gold)) + " Gold"
		},
		],
		"buttons": [
		{
		"label": "λ€",
		"action": "block",
		"blockId": "6110e28bb39c74041ad0ff68"
		},
		{
		"label": "μλμ",
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
	
	else: # μΌλ° νλ§€
		quantity = ""
		pickItem = ""
		
		if req[-1] == 'κ°':
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
			"text": "μλͺ»λ μλ ₯μ λ³΄ μλλ€"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "610e4299defb4e3121f2eb62",
			"action": "block",
			"label": "λ€μμλ ₯ βοΈ"
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
			"text": "μλͺ»λ μλ ₯μ λ³΄ μλλ€"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "610e4299defb4e3121f2eb62",
			"action": "block",
			"label": "λ€μμλ ₯ βοΈ"
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
			"description": "μμ μ λ³΄λ‘ νλ§€λ₯Ό μ§νν©λλ€",
			"profile": {
			"title": "νλ§€ μ λ³΄",
			"imageUrl": picPath.default1319
			},
			"itemList": [
			{
			"title": "μμ΄ν",
			"description": pickItem
			},
			{
			"title": "νλ§€μλ",
			"description": str(quantity) + "κ°"
			},
			{
			"title": "νλ§€κ°κ²©",
			"description": str("{:,}".format(int(pickItem_info.sellPrice * quantity))) + " Gold"
			},
			],
			"buttons": [
			{
			"label": "λ€",
			"action": "block",
			"blockId": "6110e28bb39c74041ad0ff68"
			},
			{
			"label": "μλμ",
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
		

def sellItem_yes(reqData): # νλ§€ νμ 
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	pickItem = reqData['contexts'][0]['params']['pickItem']['value']
	quantity = reqData['contexts'][0]['params']['quantity']['value']
	
	if models.ItemBook.query.filter_by(category=pickItem).first() is None: # μΌλ° νλ§€ νμ 
		itemQuery.changeAGold(pickItem, userProfile.id, quantity)
		models.db.session.commit()
	
	else: # μΌκ΄νλ§€ νμ 
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
	"text": "μ±κ³΅μ μΌλ‘ νλ§€νμμ΅λλ€"
	}
	},
	],
	"quickReplies": [
	{
	"blockId": "610e4299defb4e3121f2eb62",
	"action": "block",
	"label": "νκΈ° π«"
	},
	{
	"label": "μΈλ²€ν λ¦¬ π",
	"action": "block",
	"blockId": "6109213f3dcccc79addb1958"
	},
	]
	}
	}

	return res
	
def itemLock(reqData): # μμ΄ν μ κΈκΈ°λ₯
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
  
	fish_list = ["ν΄λ§","μμ΄", "μ°μ΄", "μ°ΈμΉ","κ°μ€λ¦¬", "λ³΅μ΄", "μμ΄", "κ³ λ±μ΄","μ€μ§μ΄", "κ½κ²", "μ±κ²"]
	req = reqData['action']['detailParams']['lockItem']['value']
	
	pickItem = models.Inventory.query.filter(models.Inventory.name==req, models.Inventory.user_id == userProfile.id).first()
	
	if pickItem is None: # μλ ₯ μμ΄νλͺμ΄ μ¬λ°λ₯΄μ§ μμλ
		for fish in fish_list: #λ¬Όκ³ κΈ°μΈμ§ νμΈ
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
			"text": "μλͺ»λ μλ ₯μ λ³΄ μλλ€"
			}
			}
			],
			"quickReplies": [
			{
			"blockId": "61137c29b39c74041ad10ec9",
			"action": "block",
			"label": "λ€μμλ ₯ βοΈ"
			},
			
			]
			}
			}
			
			return res
			
	
	# μ μ μλ ₯ νΉμ λ¬Όκ³ κΈ°
	if pickItem.lock == 1:
		pickItem.lock = 0
		answer = pickItem.name + " ν΄μ λμμ΅λλ€ π"
		
	else:
		pickItem.lock = 1
		answer = pickItem.name + " μ κ²Όμ΅λλ€ π"
		
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
	"label": "μΈλ²€ν λ¦¬ π",
	"action": "block",
	"blockId": "6109213f3dcccc79addb1958"
	},
	{
	"blockId": "61137c29b39c74041ad10ec9",
	"action": "block",
	"label": "μ κΈ π"
	}
	]
	}
	}
	
	return res
		
