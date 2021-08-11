from . import myPage
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from systemPart import loginSession
from systemPart import itemQuery
import models

def shop(reqData):
		
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
				
				"imageUrl": "http://210.111.183.149:1234/static/equipment_shop.png"
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
				"imageUrl": "http://210.111.183.149:1234/static/pet_shop.png"
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
	req = reqData['contexts'][0]['params']['user_id']['value']
	userProfile = models.User.query.filter_by(userid=req).first()
	req = reqData['userRequest']['utterance'].split(" ")[0]
	
	if req == '검': # 검 구매시
		req = str(req)+" 0강"
	
	pickItem = models.ItemBook.query.filter_by(itemName = req).first()
	if userProfile.gold < pickItem.buyPrice: # 돈 부족
		res = {
		"version": "2.0",
		"context": {
		"values": [
		{
		"name": "login_user",
		"lifeSpan": 10,
		"params": {
		"login_user": str(userProfile.userid)
		}
		}
		]
		},
		"template": {
		"outputs": [
		{
		"simpleImage": {
		"imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
		}
		},{
		"simpleText": {
		"text": "골드가 부족합니다"
		}
		}
		]
		}
		}
		return res
	
	if pickItem.itemName == '검 0강': # 검은 3개까지 이므로 구매 제한
		user_sword = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name.like('%검%'), models.Inventory.name.like('%강%')).all()
		swordCount = 0
		
		for sword in user_sword:
			swordCount += sword.quantity
			
		if swordCount >= 3:
			res = {
			"version": "2.0",
			"context": {
			"values": [
			{
			"name": "login_user",
			"lifeSpan": 10,
			"params": {
			"login_user": str(userProfile.userid)
			}
			}
			]
			},
			"template": {
			"outputs": [
			{"simpleImage": {
			"imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
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
	
	
	itemQuery.addA(pickItem.itemName,userProfile.id, 1)
	userProfile.gold -= pickItem.buyPrice
	models.db.session.commit()
	
	res = {
	"version": "2.0",
	"context": {
	"values": [
	{
	"name": "login_user",
	"lifeSpan": 10,
	"params": {
	"login_user": str(userProfile.userid)
	}
	}
	]
	},
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
	
def shop_equipment(reqData):
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
                        "imageUrl": "http://210.111.183.149:1234/static/itemResource/sword_profile.png"
			 
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
                            "label": "검 구입",
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
                        "imageUrl": "http://210.111.183.149:1234/static/itemResource/sword_profile.png"
			 
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

def shop_pet(reqData):
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
                        "imageUrl": "http://210.111.183.149:1234/static/itemResource/pet_egg.png"
			 
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
                            "label": "알 구입",
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
                        "imageUrl": "http://210.111.183.149:1234/static/itemResource/sword_profile.png"
			 
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
	
