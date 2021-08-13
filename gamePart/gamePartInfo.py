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
  "title": "강화소 💥",
  "description": "강화를 통해 최고의 장비를 만들자",
  "thumbnail": {
  "imageUrl": "http://210.111.183.149:1234/static/beef_smithy.png"
  },
  "buttons": [
  {
  "action": "block",
  "label": "이동",
  "blockId": "610e9a6fee2e484fe68ac25a"
  },
  ],
  },
  {
  "title": "동물농장 🐶",
  "description": "너무나도 귀여운 마이펫을 키워보아요",
  "thumbnail": {
  "imageUrl": "http://210.111.183.149:1234/static/pet_game.png"
  },
  "buttons": [
  {
  "action": "block",
  "label": "이동",
  "blockId": "610bcb6a401b7e060181d207"
  },
  ]
  },
  ]
  }
  }
  ]
  }
  }
  return res
