import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
from systemPart import itemQuery
from systemPart import get_kakaoKey

beePersent = [99, 90, 80, 70, 65, 60, 54, 49, 45, 42, 35, 30, 25, 22, 20, 19, 16, 14, 12, 11, 10, 9, 7, 6, 5]
beeUpgradeValues = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4]
ran_ment = ['가자.. 가보자 💥', '망치로 땅땅땅빵 🔨', '두구두구두두구⁉️']

def beefUp_select(reqData):
  systemCheck = get_kakaoKey.get_kakaoKey(reqData)
  if systemCheck != 0:
    if systemCheck == 1:
      return get_kakaoKey.res
    elif systemCheck == 2:
      return get_kakaoKey.notice(reqData)
  
		
  userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()

  user_sword = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name.like('%검%'), models.Inventory.name.like('%강%'), models.Inventory.lock == 0).all()
  swords=[]
  
  if not user_sword:
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
	"text": "강화 가능한 아이템이 없어요"
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
  else: 
    for sword in user_sword: swords.append({"label": sword.name, "action": "block", "blockId": "610a12d9d919c93e877557df" })
      
    res = {
    "version": "2.0",
    "template": {
    "outputs": [
    {
    "simpleText": {
    "text": "장비를 선택하세요 🗡"
    }
    }
    ],
    "quickReplies": swords
    }
    }
    
  return res
    
def beefUp(reqData): # 강화
  systemCheck = get_kakaoKey.get_kakaoKey(reqData)
  if systemCheck != 0:
    if systemCheck == 1:
      return get_kakaoKey.res
    elif systemCheck == 2:
      return get_kakaoKey.notice(reqData)

  
  userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
  
  if len(reqData['contexts']) > 0:
    req = reqData['contexts'][0]['params']['itemName']['value']

  else:
    req = reqData['userRequest']['utterance']

  user_sword = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name == req).first()
  itemNumber = models.ItemBook.query.filter_by(itemName = user_sword.name).first()
  beeGrade = 0
  beeGrade = int(user_sword.name.split(" ")[1][:-1])
  
  res = {
  "version": "2.0",
  "context": {
  "values": [{
  "name": "m_beef_info",
  "lifeSpan": 1,
  "params": {
  "itemName": str(user_sword.name)
  }}]
  },
  "template": {
  "outputs": [
  {
  "simpleText": {
  "text": "강화를 시도합니다"
  } 
  },
  {
  "itemCard": {
  "imageTitle": {
  "title": "강화 시도중",
  "description": "\"행운을 빈다네.\""
  },
  "title": "",
  "description": "",
  "thumbnail": {
  "imageUrl": picPath.beef_smithy,
  "width": 800,
  "height": 400
  },
  "profile": {
  "title": str(user_sword.name),
  "imageUrl": picPath.sword
  
  },
  "itemList": [
  {
  "title": "강화정보",
  "description": str(beeGrade)+"강 → " + str(beeGrade+1)+"강"
  
  },
  {
  "title": "수치변화",
  "description": "공격력 +"+str(beeUpgradeValues[beeGrade+1])
  
  },
  {
  "title": "확률",
  "description": str(beePersent[beeGrade]) + "%"
  },
  {
  "title": "강화비용",
  "description": str("{:,}".format((beeGrade+1)*1000)) + " Gold" + " (" + str("{:,}".format(userProfile.gold)) + ")"
  },
  ],
  "buttons": [
  {
  "label": "강화",
  "action": "block",
  "blockId": "610a91aa401b7e060181cc1e"
  },
  {
  "label": "취소",
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


def beefUp_try(reqData):
  
  userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
  
  req = reqData['contexts'][0]['params']['itemName']['value']
  user_sword = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name == req).first()
  beeGrade = int(user_sword.name.split(" ")[1][:-1])
  sucSword = models.ItemBook.query.filter_by(itemName = ("검 " + str(beeGrade+1) + "강")).first()
  
  if userProfile.gold > (beeGrade+1)*1000:
    userProfile.gold -= (beeGrade+1)*1000
    
    if (beePersent[beeGrade] >= random.randrange(1,101)):
      itemQuery.changeAB(user_sword.name, sucSword.itemName, userProfile.id, 1)

      res = {
      "version": "2.0",
      "context": {
      "values": [
      {
      "name": "m_beef_info",
      "lifeSpan": 1,
      "params": {
      "itemName": str(sucSword.itemName)
      }
      }
      ]
      },
      "template": {
      "outputs": [
      {
      "simpleText": {
      "text": ran_ment[random.randrange(0,3)]
      }
      },
      {
      "itemCard": {
      "imageTitle": {
      "title": "✨",
      "description": "\"어머나 더 멋있어졌어!\""
      },
      "thumbnail": {
      "imageUrl": picPath.beefSuc,
      "width": 800,
      "height": 400
      },
      "profile": {
      "title": str(sucSword.itemName),
      "imageUrl": picPath.sword
      
      },
      "itemList": [
      {
      "title": "강화정보",
      "description": str(sucSword.itemName.split(" ")[1][:-1])+"강"
      
      },
      {
      "title": "현재수치",
      "description": "공격력 " + str(sucSword.spec.split(" ")[1])
      
      },
      {
      "title": "판매가격",
      "description": str("{:,}".format(sucSword.sellPrice)) + " Gold"
      },
      ],
      "buttons": [
      {
      "label": "강화",
      "action": "block",
      "blockId": "610a12d9d919c93e877557df"
      },
      {
      "label": "🏠",
      "action": "block",
      "blockId": "6109213f3dcccc79addb1958"
      },
      ],
      "buttonLayout" : "horizontal"
      }
      }
      ]
      }
      }
	
    else:
      if user_sword.quantity == 1:
	      models.db.session.delete(user_sword)
	      
      else:
	      user_sword.quantity -= 1
      
      if beeGrade == 0:
	      itemQuery.addA("저주받은 검", userProfile.id, 1)
	
      models.db.session.commit()

      res = {
      "version": "2.0",
      "template": {
      "outputs": [
      {
      "simpleText": {
      "text": ran_ment[random.randrange(0,3)]
      }
      },
      {
      "basicCard": {
      "title": "🍎",
      "description": "아쉽지만 그렇게 됐어요",
      "thumbnail": {
      "imageUrl": picPath.beefFail
      }
      }
      }
      ]
      }
      }
  
  else: # 돈 부족할 때
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
