import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def signIn(reqData):
    req = reqData['action']['detailParams']['user_id']['value'].split()
    userProfile = models.User.query.filter_by(userid=req[0]).first()
    if userProfile is not None:
        if userProfile.password == req[1]:
            if models.UserStatus.query.filter_by(id=userProfile.id).first() is None:
                models.db.session.add(models.UserStatus(userProfile.id))
                models.db.session.commit()
    
            if userProfile.kakaoKey is None:
                userProfile.kakaoKey = str(reqData['userRequest']['user']['id'])
                models.db.session.commit()
                
            print("\n" + str(req[0]) + "님이 로그인 하셨습니다\n")
            res = {
            "version": "2.0",
            "context": {
            "values": [
            {
            "name": "login_user",
            "lifeSpan": 10,
            "params": {
            "user_id": req[0]
            }
            }
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
        else:
            res = {
    "version": "2.0",
    "context": {
    "values": [
      {
        "name": "login_user",
        "lifeSpan": 0,
        "params": {
          "login_user": None
        }
      }
    ]
    },
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "로그인 실패 🧐\n(비밀번호 틀림)"
                } 
            }
        ],
         "quickReplies": [
      {
        "blockId": "61076108a5a4854bcb94b9ba",
        "action": "block",
        "label": "다시입력 ✏️"
      }
        ]
    }
    }
    
    else:
        res = {
    "version": "2.0",
    "context": {
    "values": [
      {
        "name": "login_user",
        "lifeSpan": 0,
        "params": {
          "user_id": None
        }
      }
    ]
    },
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "로그인 실패 🧐\n(없는 아이디)"
                } 
            }
        ],
          "quickReplies": [
          {
        "blockId": "61076108a5a4854bcb94b9ba",
        "action": "block",
        "label": "다시입력 ✏️"
      },
      {
        "blockId": "610b4ae0b39c74041ad0ea22",
        "action": "block",
        "label": "회원가입 🥕"
      }
        ]
    }
    }
    return res
    
            
        
    
