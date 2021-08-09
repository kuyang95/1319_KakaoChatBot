import random
from . import words

def rdw(reqData):	# 오늘의 말씀
	req = reqData
	user_say = req["userRequest"]["utterance"]      #사용자 발화 내용
	
	a = str("싫어")
	if a in user_say:
		ans1 = str(" 이 구절부터 차근차근 시작해봐요! 화이팅!")
		ans2 = random.choice(words.random_words)
	
		randidumdi = ans1 + "\n" + ans2
	else:
		randidumdi = random.choice(words.random_words)
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"simpleText": {
	    "text": randidumdi
	}
	}
	]
	}
	}
	
	return res

def first_branch():
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "¯\_(ツ)_/¯ 더 자세히 알려줄래요? ¯\_(ツ)_/¯ "
                }
            }
        ],      #블록 생성(선택지)
         "quickReplies": [
      {
        "label": "인간 관계",    #보여질 텍스트
        "action": "block",
        "blockId": "6108bd473dcccc79addb1518",
      },
      {
        "label": "일상",
        "action": "block",
        "blockId": "6108bd473dcccc79addb1518"
      },
      {
        "label": "믿음 생활",
        "action": "block",
        "blockId": "6108bd473dcccc79addb1518" 
      }
    ]
    }
}
    return res

def second_branch(reqData):
	res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "¯\_(ツ)_/¯ 더 자세히 알려줄래요? ¯\_(ツ)_/¯ "
                }
            }
        ]
	}
	}

	return res
	
