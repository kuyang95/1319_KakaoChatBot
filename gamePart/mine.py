import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
from systemPart import itemQuery
from systemPart import loginSession

legend_ore = "다이아몬드"
epic_ore = ["에메랄드","사파이어","루비"]
uncommon_ore = ["자수정","토파즈","흑석"]
common_ore = ["구리","철","은", "돌"]
hidden_ore = ["장인의 곡괭이"]

def mine(reqData):
	if loginSession.loginSession(reqData) is not True:
		return loginSession.res
	
	userProfile = models.User.query.filter_by(userid = reqData['contexts'][0]['params']['user_id']['value']).first()
	req = ""
	for i in range(1,5):
		req += reqData['action']['params']['mine'+str(i)]
	
	if req != '으차으차':
		res = {
	"version": "2.0",
	"context": {
	    "values": [
	      {
		"name": "login_user",
		"lifeSpan": 10,
		"params": {
		  "user_id": str(userProfile.userid)
		}
		}
	    ]
		},
	"template": {
	"outputs": [
	    {
		"simpleText": {
		    "text": "채굴 실패❕"
		}
	    }
	],
	"quickReplies": [
	  {
	"blockId": "6111481f401b7e060181e789",
	"action": "block",
	"label": "채굴 🪨️"
	},
	]
	}
	}
	
		return res
	
	result = []
	
	if models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name == '장인의 곡괭이').first() is not None:
		answer = "채굴완료 [장인🔅]\n\n수고비 💰\n——————————————\n500 Gold\n\n발견한 광물 🪨\n——————————————\n"
		mineCount = 4
	else:
		answer = "채굴완료\n\n수고비 💰\n——————————————\n500 Gold\n\n발견한 광물 🪨\n——————————————\n"
		mineCount = 3
	
	for i in range(0,mineCount):
		number = random.randrange(1,5001)
		
		if number <= 2500: pass
			
		elif number <= 3000:
			result.append(random.choice(common_ore))
		
		elif number <= 4500:
			if random.randrange(1,11) == 1:
				result.append(random.choice(uncommon_ore))
			else:
				result.append(random.choice(uncommon_ore) + " 원석")
		
		elif number <= 4992:
			if random.randrange(1,11) == 1:
				result.append(random.choice(epic_ore))
			else:
				result.append(random.choice(epic_ore) + " 원석")
		
		elif number <= 4998:
			result.append(random.choice(hidden_ore))
		
		else:
			if random.randrange(1,11) == 1:
				result.append(legend_ore)
			else:
				result.append(legend_ore + " 원석")
	
	if not result:
		answer += "(없음)"
	
	else:
		for ore in result:
			userProfile.gold += 500
			itemQuery.addA(ore, userProfile.id, 1)
			models.db.session.commit()
			
		for ore in result:
			if '원석' not in ore and ore not in common_ore:
				answer += '- ' + ore + " ✨✨✨" + '\n' 
			else:
				answer += '- ' + ore + '\n' 
		


	res = {
	"version": "2.0",
	"context": {
	    "values": [
	      {
		"name": "login_user",
		"lifeSpan": 10,
		"params": {
		  "user_id": str(userProfile.userid)
		}
		}
	    ]
		},
	"template": {
	"outputs": [{
		"simpleText": {
		    "text": "채굴 진행중..💦  ■■■■  (4/4)"
		}
	    },
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
	"blockId": "6111481f401b7e060181e789",
	"action": "block",
	"label": "채굴 🪨️"
	}
	]
	}
	}
	
	return res
