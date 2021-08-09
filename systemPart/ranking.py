import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def ranking(reqData):
	now = time.localtime()
	answer = "🏆 랭킹\n" + str(time.strftime('%y-%m-%d %H:%M', time.localtime(time.time()))) +" 현재"
	

	#-------- 부자랭킹_start
	answer += "\n\n——————————————\n💰 Gold\n————————\n"
	m_query = models.User.query.order_by(models.User.gold.desc()).limit(3).all()
	
	for idx, user in enumerate(m_query,1):
		if idx == 1:
			answer += "🥇. "
		elif idx == 2:
			answer += "🥈. "
		else:
			answer += "🥉. "
		rankUserName = str(user.userid)
		answer += rankUserName + "   " + str("{:,}".format(user.gold)) + " Gold" + "\n"
			
	#-------- 부자랭킹_end
	
	
	#-------- 강화랭킹_start
	answer += "\n\n——————————————\n💥 강화\n————————\n"
	m_query = models.Inventory.query.filter(models.Inventory.name.like('%검%'), models.Inventory.name.like('%강%')).order_by(models.Inventory.itemNo.desc()).limit(3).all()
	
	for idx, user in enumerate(m_query,1):
		if idx == 1:
			answer += "🥇. "
		elif idx == 2:
			answer += "🥈. "
		else:
			answer += "🥉. "
		rankUserName = str(models.User.query.filter_by(id=user.user_id).first().userid)
		answer += rankUserName + "   " + str(user.name.split(" ")[1]) + "\n"
	#-------- 강화랭킹_end
		
		
		
	
	res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": answer
                }
            }
        ]
	}
	}
	
	return res
	
