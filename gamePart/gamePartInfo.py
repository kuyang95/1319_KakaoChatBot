import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import picPath

def gamePartInfo():
	
  res = {
  "version": "2.0",
  "template": {
  "outputs": [
  {
  "carousel": {
  "type": "basicCard",
  "items": [
  {
  "title": "κ°νμ π₯",
  "description": "κ°νλ₯Ό ν΅ν΄ μ΅κ³ μ μ₯λΉλ₯Ό λ§λ€μ",
  "thumbnail": {
  "imageUrl": picPath.beef_smithy
  },
  "buttons": [
  {
  "action": "block",
  "label": "μ΄λ",
  "blockId": "610e9a6fee2e484fe68ac25a"
  },
  ],
  },
  {
  "title": "λλ¬Όλμ₯ πΆ",
  "description": "λλ¬΄λλ κ·μ¬μ΄ λ§μ΄ν«μ ν€μλ³΄μμ",
  "thumbnail": {
  "imageUrl": picPath.petGame_thumnail
  },
  "buttons": [
  {
  "action": "block",
  "label": "μ΄λ",
  "blockId": "610bcb6a401b7e060181d207"
  },
  ]
  },
  ]
  }
  }
  ],
  "quickReplies": [
    {
    "label": "ββλ―Έλκ²μ π°",
    "action": "block",
    "blockId": "611a773aa5a4854bcb95095a"
    }
    ]
  }
  }
  return res
