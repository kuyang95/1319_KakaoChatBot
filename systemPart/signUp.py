import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def signUp(reqData):
    req = reqData
    input_text = req['action']['detailParams']['user_id']['value']

    if len(input_text) > 5 :
        res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "회원가입 실패 🧐\n(5글자 초과)"
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
        temp_pw = random.randrange(1000,10000)
        
        res = {
    "version": "2.0",
     "context": {
    "values": [
      {
        "name": "signUp",
        "lifeSpan": 1,
        "params": {
          "user_pw": temp_pw
        }
      }
    ]
	},
    "template": {
        "outputs": [
            {
                "itemCard": {
                    "description": "위의 정보로 가입을 진행합니다",
                    "profile": {
                        "title": "회원가입 정보",
                        "imageUrl": "http://210.111.183.149:1234/static/1319default.png"
                    },
                    "itemList": [
                        {
                            "title": "아이디",
                            "description": input_text
                        },
                        {
                            "title": "비밀번호",
                            "description": temp_pw
                        },
                    ],
                    "buttons": [
                        {
                            "label": "네",
                            "action": "block",
                            "blockId": "6103c8e66a30ed791b5d217b"
                        },
                        {
                            "label": "아니요",
                            "action": "block",
                            "blockId": "6110e020401b7e060181e484"
                        },
                    ],
                    "buttonLayout" : "horizontal"
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
                    "text": "회원가입 실패 🧐\n(중복된 아이디)"
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

def signUp_yes(reqData):
    req_id = reqData['action']['params']['user_id']
    req_pw = reqData['action']['params']['user_pw']
    models.db.session.add(models.User(req_id,req_pw))
    models.db.session.commit()
    userProfile = models.User.query.filter_by(userid = req_id).first()
    models.db.session.add(models.UserStatus(userProfile.id))
    models.db.session.commit()
    print("\n" + req_id, "님이 회원가입 하셨습니다\n")
    res = {
    "version": "2.0",
    "template": {
    "outputs": [
      {
        "basicCard": {
          "title": "환영합니다 ᵔࡇᵔ",
          "description": "1319의 회원이 되셨습니다 🥰",
          "thumbnail": {
            "imageUrl": "http://210.111.183.149:1234/static/1319welcome2.png"
          }
        }
      }
    ]
    }
    }
    
    return res
