import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from systemPart import get_kakaoKey
import models

def myPage(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	res = {
	"version": "2.0",
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
	"label": "인벤토리 🎒",
	"action": "block",
	"blockId": "6109213f3dcccc79addb1958"
	},
	{
	"label": "활동 🏃‍♂️",
	"action": "block",
	"blockId": "610caea93dcccc79addb2654"
	},
	{
	"label": "시스템 🎈",
	"action": "block",
	"blockId": "61150c60199a8173c6c4ab47"
	},
	
	]
	}
	}

	return res
	
