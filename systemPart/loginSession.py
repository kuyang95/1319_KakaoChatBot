import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models


		
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
	
def loginSession(reqData):
	if len(reqData['contexts']) > 0:
		req = reqData['contexts'][0]['params']['user_id']['value']
		userProfile = models.User.query.filter_by(userid=req).first()
		
		if userProfile is None:
			return False
	
	else:
		return False
	
	
	return True

def loginContext(reqData):
	contexts_data = (
		    {
		        "name": "login_user",
		        "lifeSpan": 10,
		        "params": {
		          "login_user": str(reqData['contexts'][0]['params']['user_id']['value'])
		        }
		      }
		    )
	return contexts_data
