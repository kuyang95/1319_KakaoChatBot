import sys
import os
import time
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath

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
		"text": "안녕하세요. 컨텐츠 이용을 위해서 닉네임이 필요해요\n\n"
		} 
		}
		],
		"quickReplies": [
			{
			"blockId": "610b4ae0b39c74041ad0ea22",
			"action": "block",
			"label": "닉네임 입력 ✏️️"
			},
			]	
		}
		}

def get_kakaoKey(reqData):
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	if userProfile is None:
		return 1
		
	elif str(userProfile.attendanceDate) != str(datetime.datetime.now().day):
		return 2
     
		
	return 0

def notice(reqData):
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	answer = ""
	userProfile.attendanceDate = datetime.datetime.now().day
	userProfile.loginPoint += 10
	models.db.session.commit()
	
	answer += "💎 출석포인트 10점 획득"
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"itemCard": {
	"title": "동물농장 펫 먹이주기, 학교보내기 구현",
	"imageTitle": {
	"title": "✨",
	"description": "환영합니다"
	},
	"thumbnail": {
	"imageUrl": picPath.notice_thumbnail,
	"width": 800,
	"height": 800
	},
	"profile": {
	"title": "NOTICE",
	"imageUrl": picPath.default1319
	
	},
	"itemList": [
	{
	"title": "업데이트 날짜",
	"description": "9월 1일"
	},
	],
	"buttons": [
	{
	"label": "패치노트",
	"action": "block",
	"blockId": "610bcb6a401b7e060181d207"
	},
	{
	"label": "개발자 근황",
	"action": "block",
	"blockId": "610bcb6a401b7e060181d207"
	},
	],
	"buttonLayout" : "horizontal"
	}
	},
	{
	"simpleText": {
	"text": answer
	}
	},
	],
	"quickReplies": [
		{
		"messageText": "훈련센터",
		"action": "message",
		"label": "업데이트된 훈련센터로 이동  🥬"
		},
		]
	}
	}

	return res
	
def makeNickname(reqData):
	req = reqData
	input_text = req['action']['detailParams']['nickname']['value']
	
	if len(input_text) > 7 :
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": "등록실패 🧐\n(7글자 초과)"
		} 
		}
		],
		"quickReplies": [
		{
		"blockId": "610b4ae0b39c74041ad0ea22",
		"action": "block",
		"label": "다시입력 ✏️"
		}
		]
		}
		}
	
	elif models.User.query.filter_by(userid=input_text).first() is None:     
		
		models.db.session.add(models.User(input_text, reqData['userRequest']['user']['id']))
		models.db.session.commit()
		userProfile = models.User.query.filter_by(userid = input_text).first()
		models.db.session.add(models.UserStatus(userProfile.id))
		models.db.session.commit()
		print("\n" + input_text, "님이 회원가입 하셨습니다\n")
		
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"basicCard": {
		"title": "환영합니다 ᵔࡇᵔ",
		"description": "\"" + input_text + "\"" + " 닉네임이 등록되었습니다 🥰",
		"thumbnail": {
		"imageUrl": "http://210.111.183.149:1234/static/1319welcome2.png"
		}
		}
		}
		]
		}
		}
	
	else:
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": "등록실패 🧐\n(중복된 닉네임)"
		}
		}
		],
		"quickReplies": [
		{
		"blockId": "610b4ae0b39c74041ad0ea22",
		"action": "block",
		"label": "다시입력 ✏️"
		}
		]
		}
		}
		
	return res
	
