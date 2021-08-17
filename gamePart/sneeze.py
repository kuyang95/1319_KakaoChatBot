import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
from sqlalchemy import or_
from systemPart import itemQuery
from systemPart import get_kakaoKey


def sneeze_index(reqData):
	if get_kakaoKey.get_kakaoKey(reqData) is not True:
		return get_kakaoKey.res
		
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	
	roomCheck = models.MultiRoom.query.filter(or_(models.MultiRoom.player1 == userProfile.userid, models.MultiRoom.player2 == userProfile.userid)).first()
	if roomCheck:
		if roomCheck.player1 == userProfile.userid:
			models.db.session.delete(roomCheck)
			models.db.session.commit()
			
		else:
			roomCheck.player2 = None
			models.db.session.commit()
			
	answer = "기침재판 ⚜️\n\n번호/방제/방장\n\n"
	buttons = []
	buttons.append({
		"blockId": "611b12ba401b7e0601820cae",
		"action": "block",
		"label": "게임설명 📝"
		})
	buttons.append({
		"blockId": "611b12ba401b7e0601820cae",
		"action": "block",
		"label": "입장하기 🚪"
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
	if buttonName == '입장하기':
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
			"blockId": "6110e020401b7e060181e484",
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
			"blockId": "6110e020401b7e060181e484",
			"action": "block",
			"label": "새로고침 💫"
			}
			]
			}
			}
			
			return res
	
	else:
		res = {
		"version": "2.0",
		"template": {
		"outputs": [
		{
		"simpleText": {
		"text": "hi"
		} 
		}
		],
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
		
			
