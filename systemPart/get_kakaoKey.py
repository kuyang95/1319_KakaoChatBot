import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

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
	req = reqData['userRequest']['user']['id']

	if models.User.query.filter_by(kakaoKey=req).first() is None:
		return False
		
		
	return True

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
	
