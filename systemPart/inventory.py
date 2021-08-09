import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from systemPart import loginSession
from systemPart import itemQuery
import models

def inventory(reqData):
	if loginSession.loginSession(reqData) is not True:
		return loginSession.res
		
	req = reqData['contexts'][0]['params']['user_id']['value']
	userProfile = models.User.query.filter_by(userid=req).first()
	user_inven = models.Inventory.query.filter_by(user_id=userProfile.id).all()
	answer = ""
	answer += "💰: "+ str("{:,}".format(int(userProfile.gold))) + " Gold\n"
	answer += "💎: "+ str("{:,}".format(int(userProfile.loginPoint))) + " p\n\n"
	if len(user_inven) == 0:
		res = {
    "version": "2.0",
    "context": {
		    "values": [
		      {
		        "name": "login_user",
		        "lifeSpan": 10,
		        "params": {
		          "user_id": str(req)
		        }
		      }
		    ]
			},
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

	else:
		
		for inven in user_inven:
			answer += "- " + inven.name + "   " + str(inven.quantity) + "\n"

		res = {
    "version": "2.0",
    "context": {
		    "values": [
		      {
		        "name": "login_user",
		        "lifeSpan": 10,
		        "params": {
		          "user_id": str(req)
		        }
		      }
		    ]
			},
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
      }
        ]
	}
	}
	
	return res
	
def viewItemDescript(reqData):
	req = reqData['action']['detailParams']['select_item']['value']
	
	pickItem = models.ItemBook.query.filter_by(itemName=req).first()
	userProfile = models.User.query.filter_by(userid = reqData['contexts'][0]['params']['user_id']['value']).first()
	
	if pickItem is None:
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
	"simpleImage": {
	                    "imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
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
		"itemCard":{
		 "imageTitle": {
                        "title": "No. " + str(pickItem.id),
                        "description": "도감번호"
                    },
			"title": "설명",
			    "description": pickItem.descript,
			    "profile": {
				"title": item_name,
				"imageUrl": "http://210.111.183.149:1234/static/sword_profile.png"
				 
			    },
			    "itemList": [
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

def sellItem(reqData):
	req = reqData['action']['detailParams']['sell_info']['value']
	userProfile = models.User.query.filter_by(userid=reqData['contexts'][0]['params']['user_id']['value']).first()
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
	                    "imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
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
	"blockId": "610fc056a5a4854bcb94d908",
	"action": "block",
	"label": "다시입력 ✏️"
	},
	
	]
	}
	}
	
	for itemPuzzle in req[:-1]:
		pickItem += itemPuzzle
	
	pickItem = pickItem[:-1]
	
	userItem = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name==pickItem).first()
	
	if userItem is None or userItem.quantity < quantity:
		res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	                "simpleImage": {
	                    "imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
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
	"blockId": "610fc056a5a4854bcb94d908",
	"action": "block",
	"label": "다시입력 ✏️"
	},
	
	]
	}
	}
	
	else:
		pickItem_info = models.ItemBook.query.filter_by(itemName = pickItem).first()
		res = {
    "version": "2.0",
     "context": {
    "values": [
      {
        "name": "login_user",
        "lifeSpan": 10,
        "params": {
          "user_id": userProfile.userid
        }
      },
       {
        "name": "n_sell_info",
        "lifeSpan": 1,
        "params": {
          "pickItem": pickItem_info.itemName,
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
                        "imageUrl": "http://210.111.183.149:1234/static/1319default.png"
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
		

def sellItem_yes(reqData):
	req = reqData['contexts'][0]['params']['user_id']['value']
	userProfile = models.User.query.filter_by(userid=req).first()
	
	pickItem = reqData['contexts'][1]['params']['pickItem']['value']
	quantity = reqData['contexts'][1]['params']['quantity']['value']
	
	if itemQuery.changeAGold(pickItem, userProfile.id, quantity):
		res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	                "simpleImage": {
	                    "imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
	                }
	                },
	    {
		"simpleText": {
		    "text": "성공적으로 판매하였습니다"
		}
	    }
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
	
