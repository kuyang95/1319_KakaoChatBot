import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def attendance(reqData):
	req = reqData['contexts'][0]['params']['user_id']['value']
	userProfile = models.User.query.filter_by(userid=req).first()
	if str(userProfile.attendanceDate) != str(datetime.datetime.now().day):
		print(userProfile.attendanceDate, datetime.datetime.now().day)
		userProfile.attendanceDate = datetime.datetime.now().day
		userProfile.loginPoint += 10
		models.db.session.commit()
		
		res = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "basicCard": {
          "title": "출석체크 완료❕",
          "description": "보유 포인트: " + str(userProfile.loginPoint) + "p",
          "thumbnail": {
            "imageUrl": "http://210.111.183.149:1234/static/attendance.png"
          }
        }
      }
    ]
  }
}
	else:
		res = {
    "version": "2.0",
    "template": {
        "outputs": [{
	                "simpleImage": {
	                    "imageUrl": "http://210.111.183.149:1234/static/system_ment.png",
	                }
	                },
            {
                "simpleText": {
                    "text": "오늘은 이미 출석체크완료!\n내일 다시 시도해주세요"
                }
            }
        ]
    }
    }

	return res
