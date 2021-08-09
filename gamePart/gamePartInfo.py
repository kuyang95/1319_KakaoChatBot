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
                  "blockId": "60e6cd1a7d19482b2b9e794b"
                },
              ],
            },
            {
            "title": "준비중..",
			"description": "준비중",
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/1319default.png"
              },
              "buttons": [
                {
                  "action": "block",
                  "label": "이동",
                  "blockId": "61076108a5a4854bcb94b9ba"
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
