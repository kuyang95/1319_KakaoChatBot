import sys
import os
import random
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import picPath
import models
from systemPart import itemQuery
from systemPart import get_kakaoKey

def hatching(reqData): # 부화소 입력 시
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	userSt = models.UserStatus.query.filter_by(models.UserStatus.id=userProfile.id).first()
	
	if userSt.hatching == 1: #부화 진행중일때
		current_time = datetime.datetime.now()
		old_time = userSt.hatchingTimer
		time_flows = current_time - oldtime
		
		if time_flows.seconds > 144000: # 부화 완료
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
			"basicCard": {
			"title": "부화 완료❗️",
			"description": "두근두근... 뭐가 나올까",
			"thumbnail": {
			"imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
			},
			"buttons": [
			{
			  "action": "message",
			  "label": "열어보기",
			  "messageText": "짜잔! 우리가 찾던 보물입니다"
			}
			]
			}
			}
			]
			}
			}
			
		else: # 부화 진행중
			ramining_time = 144000 - time_flows.seconds
			hours = remaining_time // 3600
			s = remaining_time - hours*3600
			mu = s // 60
			ss = s - mu*60
			remaining_time = hours, '시간', mu, '분', ss, '초  남았습니다'
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
			"simpleImage": {
			"imageUrl": picPath.system_ment
			}
			},
			{
			"simpleText": {
			"text": "부화중.. ✨\n" + remaining_time
			} 
			}
			],
			}
			}
	else: # 부화중인게 없을 때
		user_egg = models.Inventory.query.filter(models.Inventory.name=='알', models.Inventory.user_id == userProfile.id).all()
		
		if not user_egg: # 보유 알이 없을 때
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
			"simpleImage": {
			"imageUrl": picPath.system_ment,
			}
			},
			{
			"simpleText": {
			"text": "부화 가능한 알이 없어요"
			} 
			}
			],
			"quickReplies": [
			{
			"label": "상점으로 이동 🛒",
			"action": "block",
			"blockId": "6109219c25cb590ace33a6cf"
			
			}
			]
			}
			}
		else: # 보유 알이 있을 때
			eggs = []
			for egg in user_egg: eggs.append({"label": egg.name, "action": "block", "blockId": "610a12d9d919c93e877557df" })
			
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
			"text": "부화할 알을 선택하세요 🥚"
			}
			}
			],
			"quickReplies": eggs
			}
			}
		
	return res

def hatchingFinish(reqData):
	legend_ore = "다이아몬드"
	epic_ore = ["에메랄드","사파이어","루비"]
	uncommon_ore = ["자수정","토파즈","흑석"]
	common_ore = ["구리","철","은", "돌"]
