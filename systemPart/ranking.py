import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def ranking(reqData):
	now = time.localtime()
	
	answer = "š ė­ķ¹\n" + str(time.strftime('%y-%m-%d %H:%M', time.localtime(time.time()))) +" ķģ¬"
	

	#-------- ė¶ģė­ķ¹_start
	answer += "\n\nāāāāāāāāāāāāāā\nš° ź³Øė\nāāāāāāāā\n"
	m_query = models.User.query.order_by(models.User.gold.desc()).limit(3).all()
	
	for idx, user in enumerate(m_query,1):
		if idx == 1:
			answer += "š„. "
		elif idx == 2:
			answer += "š„. "
		else:
			answer += "š„. "
		rankUserName = str(user.userid)
		answer += rankUserName + "   " + str("{:,}".format(user.gold)) + " Gold" + "\n"
			
	#-------- įį®įį”ė­ķ¹_end
	
	
	#-------- ź°ķė­ķ¹_start
	answer += "\nāāāāāāāāāāāāāā\nš„ ź°ķ\nāāāāāāāā\n"
	m_query = models.Inventory.query.filter(models.Inventory.name.like('%ź²%'), models.Inventory.name.like('%ź°%')).order_by(models.Inventory.itemNo.desc()).limit(3).all()
	
	for idx, user in enumerate(m_query,1):
		if idx == 1:
			answer += "š„. "
		elif idx == 2:
			answer += "š„. "
		else:
			answer += "š„. "
		rankUserName = str(models.User.query.filter_by(id=user.user_id).first().userid)
		answer += rankUserName + "   " + str(user.name.split(" ")[1]) + "\n"
	#-------- ź°ķė­ķ¹_end
	
	#-------- ėģė­ķ¹_start
	answer += "\nāāāāāāāāāāāāāā\nš£ ėģ\nāāāāāāāā\nMAX\n"
	m_query = models.Inventory.query.filter(models.Inventory.value.like('%cm%')).order_by(models.db.cast(models.Inventory.value, models.db.Float).desc()).limit(3).all()

	for idx, user in enumerate(m_query,1):
		if idx == 1:
			answer += "š„. "
		elif idx == 2:
			answer += "š„. "
		else:
			answer += "š„. "
		rankUserName = str(models.User.query.filter_by(id=user.user_id).first().userid)
		answer += rankUserName + "   " + user.name + "  " + user.value + "\n"
	
	answer += "\nMIN\n"
	m_query = models.Inventory.query.filter(models.Inventory.value.like('%cm%')).order_by(models.db.cast(models.Inventory.value, models.db.Float)).limit(3).all()
	
	for idx, user in enumerate(m_query,1):
		if idx == 1:
			answer += "š„. "
		elif idx == 2:
			answer += "š„. "
		else:
			answer += "š„. "
		rankUserName = str(models.User.query.filter_by(id=user.user_id).first().userid)
		answer += rankUserName + "   " + user.name + "  " + user.value + "\n"
	#-------- ėģė­ķ¹_end
		
		
		
	
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
	
