import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
import datetime
from sqlalchemy import or_
from systemPart import itemQuery
from systemPart import get_kakaoKey


def sneeze_index(reqData):
	systemCheck = get_kakaoKey.get_kakaoKey(reqData)
	if systemCheck != 0:
		if systemCheck == 1:
			return get_kakaoKey.res
		elif systemCheck == 2:
			return get_kakaoKey.notice(reqData)
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	roomCheck = models.MultiRoom.query.filter(or_(models.MultiRoom.player1 == userProfile.userid, models.MultiRoom.player2 == userProfile.userid)).first()
	if roomCheck is not None:
		if roomCheck.player1 == userProfile.userid:
			models.db.session.delete(roomCheck)
			models.db.session.commit()
			
		else:
			roomCheck.player2 = None
			models.db.session.commit()
	
	roomCheck2 = models.MultiRoom.query.filter(models.MultiRoom.createTime != None).all() # 1시간 이상된 방 폭파
	if roomCheck2: 
		current_time = datetime.datetime.now()
		for room in roomCheck2:
			room_time = datetime.datetime.strptime(room.createTime, "%Y-%m-%d %H:%M:%S.%f") # str 을 datetime 형태로 바꿔줌
			del_time = current_time - room_time
			if del_time.days*86400 + del_time.seconds > 3600:
				models.db.session.delete(room)
				models.db.session.commit()
			
		
			
	answer = "기침재판 ⚜️\n\n번호/방제/방장\n\n"
	buttons = []
	buttons.append({
		"blockId": " ",
		"action": "block",
		"label": "게임설명 📝"
		})
	buttons.append({
		"blockId": "611b12ba401b7e0601820cae",
		"action": "block",
		"label": "입장하기 🚪"
		})
	buttons.append({
		"blockId": "611a78a425cb590ace33ebb5",
		"action": "block",
		"label": "새로고침 💫"
		})	
	
	rooms = models.MultiRoom.query.filter(models.MultiRoom.player2 == None, models.MultiRoom.isGame == 0, models.MultiRoom.gameName=='sneeze').all()
	
		
	for room in rooms:
		answer += str(room.id) + ") " + room.roomName + "   " + room.player1 + "\n"
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"simpleText": {
	"text": answer
	} 
	}
	],
	"quickReplies": buttons
	}
	}
		
	return res

def sneeze_onclick(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	buttonName = reqData['userRequest']['utterance'].split(" ")[0]
	
	ran_name = ['콜록콜록', '즐거운 게임해요', '베테랑 대기중', '금부장!', '누구인가?', '초보에요..']
	if buttonName == '입장하기': # 입장하기 눌렀을 때
		inputId = reqData['action']['params']['roomId']
		if models.MultiRoom.query.filter(models.MultiRoom.id == inputId, models.MultiRoom.isGame == 0, models.MultiRoom.player2 == None, models.MultiRoom.gameName == "sneeze").first() is None:
			models.db.session.add(models.MultiRoom(userProfile.userid, "sneeze"))
			models.db.session.commit()
			room_info = models.MultiRoom.query.filter(models.MultiRoom.player1 == userProfile.userid).first()
			room_info.roomName = random.choice(ran_name)
			models.db.session.commit()
			answer = "방번호: " + str(room_info.id) + "\n" + "방제: " + str(room_info.roomName) + "\n\n" + "멤버 ♟\n——————————————\n" + str(userProfile.userid) + "\n\n" 
			res = {
			"version": "2.0",
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
			"blockId": "611a78a425cb590ace33ebb5",
			"action": "block",
			"label": "나가기 🤳️"
			},
			{
			"blockId": "611bdaeda5a4854bcb950e32",
			"action": "block",
			"label": "새로고침 💫"
			}
			]
			}
			}
			
			return res
			
		else:
			room = models.MultiRoom.query.filter(models.MultiRoom.id == inputId).first()
			room.player2 = userProfile.userid
			models.db.session.commit()
	
			answer = "방번호: " + str(room.id) + "\n" + "방제: " + str(room.roomName) + "\n\n" + "멤버 ♟\n——————————————\n" + room.player1 + "\n" + room.player2 + "\n\n" 
			res = {
			"version": "2.0",
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
			"blockId": "611a78a425cb590ace33ebb5",
			"action": "block",
			"label": "나가기 🤳️"
			},
			{
			"blockId": "611bdaeda5a4854bcb950e32",
			"action": "block",
			"label": "새로고침 💫"
			}
			]
			}
			}
			
			return res
	
	elif buttonName == '새로고침' or buttonName == '응답확인': # 새로고침 눌렀을 때
		room= models.MultiRoom.query.filter(or_(models.MultiRoom.player1 == userProfile.userid, models.MultiRoom.player2 == userProfile.userid)).first()
		
		if room is None: # 방장 나가서 방 없음
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleImage": {
			"imageUrl": picPath.system_ment,
			}
			},
			{
			"simpleText": {
			"text": "방이 없어졌습니다"
			} 
			}
			],
			"quickReplies": [
			{
			"blockId": "611a78a425cb590ace33ebb5",
			"action": "block",
			"label": "나가기 🤳️"
			}
			]
			}
			}
				
			return res
		
		else: # 시작 대기중
			if room.isGame == 0: # 대기중인 상태
				buttons = []
				buttons.append({
				"blockId": "611a78a425cb590ace33ebb5",
				"action": "block",
				"label": "나가기 🤳️"
				})
				buttons.append({
				"blockId": "611bdaeda5a4854bcb950e32",
				"action": "block",
				"label": "새로고침 💫"
				})
				
				if room.player1 == userProfile.userid and room.player2 is not None:
					buttons.append({
				"blockId": " ",
				"action": "block",
				"label": "게임시작 👈"
				})
			
				answer = "방번호: " + str(room.id) + "\n" + "방제: " + str(room.roomName) + "\n\n" + "멤버 ♟\n——————————————\n" + room.player1 + "\n" + room.player2 + "\n\n" 
				res = {
				"version": "2.0",
				"template": {
				"outputs": [
				{
				"simpleText": {
				"text": answer
				} 
				}
				],
				"quickReplies": buttons
				}
				}
				
				return res
			
			elif room.isGame == 1: # 방장이 게임시작 누른 뒤
				game_info = models.SneezeGame.query.filter(or_(models.SneezeGame.player2 == userProfile.userid, models.SneezeGame.player1 == userProfile.userid)).first()
				if room.player2 == userProfile.userid: # player2 입장				
					game_info.player2_turn += 1
					models.db.session.commit()
					
					res = {
					"version": "2.0",
					"template": {
					"outputs": [
					{
					"simpleText": {
					"text": "게임을 시작합니다"
					} 
					}
					],
					"quickReplies": [{
					"blockId": " ",
					"action": "block",
					"label": "재판장 입장 🚪"
					}
					]
					}
					}
					return res
				elif room.player1 == userProfile.userid: # player1 입장
					if game_info.player2_turn == 0: # player2 준비됨
						res = {
						"version": "2.0",
						"template": {
						"outputs": [
						{
						"simpleText": {
						"text": "게임을 시작합니다"
						} 
						}
						],
						"quickReplies": [{
						"blockId": " ",
						"action": "block",
						"label": "재판장 입장 🚪"
						}
						]
						}
						}
						return res
					else: # player2 준비안됨
						res = {
						"version": "2.0",
						"template": {
						"outputs": [
						{
						"simpleText": {
						"text": "상대방의 입력을 기다리는중.. 💭"
						} 
						}
						],
						"quickReplies": [{
						"blockId": "611bdaeda5a4854bcb950e32",
						"action": "block",
						"label": "응답확인 🎲"
						}
						
						]
						}
						}
							
						return res
					
				
				
	elif buttonName == '게임시작': # 게임시작 눌렀을 때
		room= models.MultiRoom.query.filter(models.MultiRoom.player1 == userProfile.userid).first()
		if room.player2 is not None:
			models.db.session.add(models.SneezeGame(room.id, room.player1, room.player2))
			models.db.session.commit()
			game_info = models.SneezeGame.query.filter_by(player1 = userProfile.userid).first()
			game_info.player1_turn += 1
			models.db.session.commit()
			
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": "상대방의 입력을 기다리는중.. 💭"
			} 
			}
			],
			"quickReplies": [{
			"blockId": "611bdaeda5a4854bcb950e32",
			"action": "block",
			"label": "응답확인 🎲"
			}
			
			]
			}
			}
				
			return res
		
		else: # 게임시작 눌렀는데 상대 없을 때
			buttons = []
			buttons.append({
			"blockId": "611a78a425cb590ace33ebb5",
			"action": "block",
			"label": "나가기 🤳️"
			})
			buttons.append({
			"blockId": "611bdaeda5a4854bcb950e32",
			"action": "block",
			"label": "새로고침 💫"
			})
			
			if room.player1 == userProfile.userid and room.player2 is not None:
				buttons.append({
				"blockId": " ",
				"action": "block",
				"label": "게임시작 👈"
				})
			
			answer = "방번호: " + str(room.id) + "\n" + "방제: " + str(room.roomName) + "\n\n" + "멤버 ♟\n——————————————\n" + room.player1 + "\n" + room.player2 + "\n\n" 
			res = {
			"version": "2.0",
			"template": {
			"outputs": [
			{
			"simpleText": {
			"text": answer
			} 
			}
			],
			"quickReplies": buttons
			}
			}
			
			return res
			
		
# 611b314425cb590ace33ed93

def sneeze(reqData):
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	user_utterance = reqData['userRequest']['utterance'].split(" ")[0]
	room_info = models.MultiRoom.query.filter(or_(models.MultiRoom.player1 == userProfile.userid, models.MultiRoom.player2 == userProfile.userid)).first()
	
	#if room_info is None:
		
	#if room_info.isGame == 0:
		
		
	return res
	
	#elif user_utterance == ''
		

def sneeze_judge(reqData, game_info, player):
	j_start_ment = ["양측 변호인은 진실만을 말할 것을 선서하세요"]
	p_start_ment = ["선서합니다"]
	text = ""
		
	answers = []
	answer.append({
			"simpleImage": {
			"imageUrl": picPath.trial,
			}
			}
			)
	answer.append({
			"simpleText": {
			"text": text
			} 
			})
			
	buttons = []
	buttons.append({
				"blockId": " ",
				"action": "block",
				"label": "조사 🔎"
				})
	buttons.append({
				"blockId": " ",
				"action": "block",
				"label": "방어 🔰"
				})
	buttons.append({
				"blockId": " ",
				"action": "block",
				"label": "의혹제기 🗯 "
				})		
	
	
	req = reqData['userRequest']['utterance'].split(" ")[0]
	if req == '재판장': # 게임시작
		text = "재판관 (👨‍⚖️)\n💬:"+ random.choice(j_start_ment) +"\n\n" + game_info.player1 + " ("
		for i in range(0,game_info.player1_hp):
			text += "⚜️"
		text += " "
		for i in range(0, game_info.player1_power):
			text += "🧩"
		text += ")\n💬:" + random.choice(p_start_ment)
		
		for i in range(0,game_info.player2_hp):
			text += "⚜️"
		text += " "
		for i in range(0, game_info.player2_power):
			text += "🧩"
		text += ")\n💬:" + random.choice(p_start_ment)
		
		return answer, buttons
	
	elif req == '응답확인':
		if player == 1:
			game_info.player1_time = str(datetime.datetime.now())
		else:
			game_info.player2_time = str(datetime.datetime.now())
	
	
	else: # 인게임에서 버튼 클릭시
		current_time = datetime.datetime.now()
		if player == 1:
			game_info.player1_action = req
			game_info.player1_turn += 1
			player1_time = datetime.datetime.strptime(game_info.player1_time, "%Y-%m-%d %H:%M:%S.%f") # str 을 datetime 형태로 바꿔줌
			del_time = current_time - player1_time
			if del_time.seconds > 60:
				text = "시간초과로 패배하였습니다"
				return answer, buttons
			else:
				game_info.player1_time = str(datetime.datetime.now())
			
		else:
			game_info.player2_action = req
			game_info.player2_turn += 1
			game_info.player2_time = str(datetime.datetime.now())
			player2_time = datetime.datetime.strptime(game_info.player2_time, "%Y-%m-%d %H:%M:%S.%f") # str 을 datetime 형태로 바꿔줌
			del_time = current_time - player2_time
			if del_time.seconds > 60:
				text = "시간초과로 패배하였습니다"
				return answer, buttons
			else:
				game_info.player2_time = str(datetime.datetime.now())
			
	
	#if game_info.player1_turn == game_info.gameTurn and game_info.player2_turn == game_info.gameTurn: # 플레이어 두명 다 선택 완료
		
