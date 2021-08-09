from . import myPage
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def shop(reqData):
	if len(reqData['contexts']) > 0:
		req = reqData['contexts'][0]['params']['user_id']['value']
		userProfile = models.User.query.filter_by(userid=req).first()
		res = {
	    "version": "2.0",
	    "context": {
		    "values": [
		      {
		        "name": "login_user",
		        "lifeSpan": 10,
		        "params": {
		          "login_user": str(req)
		        }
		      }
		    ]
			},
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
	            "description": "준비중..",
	              "thumbnail": {
	                "imageUrl": "http://210.111.183.149:1234/static/1319default.png"
	              },
	              "buttons": [
	                {
	                  "action": "block",
	                  "label": "이동",
	                  "blockId": "610bcb6a401b7e060181d207"
	                },
	              ]
	            },
	                    
	          ]
	        }
	        }
	        ]   
	        }
	        }
	else:
		res = myPage.myPage(reqData)


	return res


def buyAnEquipment(reqData):
	req = reqData['contexts'][0]['params']['user_id']['value']
	userProfile = models.User.query.filter_by(userid=req).first()
	req = reqData['userRequest']['utterance'].split(" ")[0]
	
	# 검 구매시
	if req == '검':
		req = str(req)+" 0강"
		pickItem = models.ItemBook.query.filter_by(itemName = req).first()
		user_sword = models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name.like('%검%'), models.Inventory.name.like('%강%')).all()
		sword_count = 0
		
		for sword in user_sword:
			sword_count += sword.quantity
		
		if userProfile.gold < pickItem.buyPrice:
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
		
		elif sword_count >=0 and sword_count <3 :
			userProfile.gold -= pickItem.buyPrice
			if models.Inventory.query.filter(models.Inventory.user_id==userProfile.id, models.Inventory.name.like('%검 0강%')).count() == 0:
				models.db.session.add(models.Inventory(pickItem.itemName, userProfile.id, pickItem.id))
				models.db.session.commit()
			
			else:
				user_0sword = models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name.like('%검 0강%')).first()
				user_0sword.quantity += 1
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
			
			
				
		else:
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
	
def shop_equipment(reqData):
	if len(reqData['contexts']) > 0:
		req = reqData['contexts'][0]['params']['login_user']['value']
		userProfile = models.User.query.filter_by(userid=req).first()
		res = {
    "version": "2.0",
     "context": {
    "values": [
      {
        "name": "login_user",
        "lifeSpan": 10,
        "params": {
          "user_pw": str(userProfile.userid)
        }
      }
    ]
	},
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
                        "imageUrl": "http://210.111.183.149:1234/static/sword_profile.png"
			 
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
                        "imageUrl": "http://210.111.183.149:1234/static/sword_profile.png"
			 
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
        
	
	else:
		res = myPage.myPage(reqData)
		
	return res
	
	
