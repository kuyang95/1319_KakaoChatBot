def welcome(): #웰컴블록
  res = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "carousel": {
          "type": "basicCard",
          "items": [
            {
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/info_egg.png"
              },
              "buttons": [
                {
                  "action": "block",
                  "label": "이동",
                  "blockId": "60e6cd1a7d19482b2b9e794b"
                },
              ]
            },
            {
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/game_egg.png"
              },
              "buttons": [
                {
                  "action": "block",
                  "label": "이동",
                  "blockId": "610c925125cb590ace33b354"
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
  
def quick_menu(): #기능부분 바로가기메뉴
  res = {
    "version": "2.0",
    "template": {
      "outputs": [
      {
        "carousel": {
          "type": "basicCard",
          "items": [
            {
              "thumbnail": {
    
                "imageUrl": "http://210.111.183.149:1234/static/weather.png"
              },
              "buttons": [
                {
                  "action": "block",
                  "label": "날씨 확인하기",
                  "blockId": "60e6cd1a7d19482b2b9e794b"
                },
              ]
            },
            {
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/music.png"
              },
              "buttons": [
                {
                  "messageText": "음원 차트",
                  "action": "message",
                  "label": "음원 차트"
                },
              ]
            },
            {
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/movie.png"
              },
              "buttons": [
                {
                  "messageText": "영화 상영작",
                  "action": "message",
                  "label": "영화 상영작"
                },
              ]
            },
            {
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/movie_soon.png"
              },
              "buttons": [
                {
                  "messageText": "개봉예정 영화",
                  "action": "message",
                    "label": "개봉예정 영화"
                },
              ]
            },
            {
              "thumbnail": {
                "imageUrl": "http://210.111.183.149:1234/static/corona.png"
              },
              "buttons": [
                {
                   "messageText": "코로나",
                    "action": "message",
                    "label": "코로나 확진자수"
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
