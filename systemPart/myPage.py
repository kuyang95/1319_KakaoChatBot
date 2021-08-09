import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def myPage(reqData):
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
		          "user_id": str(req)
		        }
		      }
		    ]
			},
		    "template": {
		        "outputs": [
		            {
		                "simpleText": {
		                    "text": "\"" + userProfile.userid + "\"" + "님의 마이페이지 🔓"
		                } 
		            }
		        ],
						"quickReplies": [
					  {
						"label": "출석 ✔️",
						"action": "block",
						"blockId": "6107cb16401b7e060181c115"
					  },
					  {
						"label": "인벤토리 🎒",
						"action": "block",
						"blockId": "6109213f3dcccc79addb1958"
					  },
					  {
				            "label": "돈벌기 💰",
				            "action": "block",
				            "blockId": "610caea93dcccc79addb2654"
				            },
					  
						]
						}
						}
		
	else:
		res = {
		  "version": "2.0",
		  "template": {
			"outputs": [
			  {
				"basicCard": {
				  "title": "1319",
				  "description": "로그인이 필요한 서비스입니다",
				  "thumbnail": {
					"imageUrl": "http://210.111.183.149:1234/static/1319default.png"
				  },
				  "buttons": [
					{
					  "action": "block",
					  "label": "로그인",
					  "blockId": "61076108a5a4854bcb94b9ba"
					},
					{
					  "action":  "block",
					  "label": "회원가입",
					  "blockId": "610b4ae0b39c74041ad0ea22"
					}
				  ]
				}
			  }
			]
		  }
		}

	return res
	
