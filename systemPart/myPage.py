import sys
import os
import datetime


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from systemPart import get_kakaoKey
import models

def myPage(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
	
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	output = []
	
	if str(userProfile.attendanceDate) != str(datetime.datetime.now().day):
		userProfile.attendanceDate = datetime.datetime.now().day
		userProfile.loginPoint += 10
		models.db.session.commit()
		
		output.append({
		"simpleText": {
		"text": "(출석포인트를 획득하였습니다 💎)"
		} 
		})
	
	output.append({
	"simpleText": {
	"text": "\"" + userProfile.userid + "\"" + "님의 마이페이지 🔓\n[칭호 없음]"
	} 
	})
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": output,
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
	"label": "시스템 🕹",
	"action": "block",
	"blockId": "61150c60199a8173c6c4ab47"
	},
	
	]
	}
	}

	return res
	
