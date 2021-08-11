import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from systemPart import loginSession
import models

def myPage(reqData):
	if loginSession.loginSession(reqData) is not True:
		return loginSession.res
	else:
		login_context = loginSession.loginContext(reqData)
		
	req = reqData['contexts'][0]['params']['user_id']['value']
	userProfile = models.User.query.filter_by(userid=req).first()
	res = {
	    "version": "2.0",
	    "context": {
	    "values": [
	      login_context
	      ]
	      },
	      
	    "template": {
	        "outputs": [
	            {
	                "simpleText": {
	                    "text": "\"" + userProfile.userid + "\"" + "님의 마이페이지 🔓\n[칭호 없음]"
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

	return res
	
