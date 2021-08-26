import sys
import os
import random
from sqlalchemy import or_


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models
import picPath
from systemPart import itemQuery
from systemPart import get_kakaoKey

def growing_eat(reqData): # 펫 레벨업
	
	print("come")
	userProfile = models.User.query.filter_by(kakaoKey=reqData['userRequest']['user']['id']).first()
	userSt = models.UserStatus.query.filter_by(id = userProfile.id).first()
	pet = models.GrowingPet.query.filter_by(id= userSt.growing_select).first()
	pet_info = models.PetBook.query.filter_by(name = pet.name).first()
	
	fishes = []
	food_list = pet_info.food.split(" ")
	fish_weight = 0
	
	fishes = models.Inventory.query.filter(models.Inventory.user_id == userProfile.id, models.Inventory.name.in_(food_list), models.Inventory.lock == 0).order_by(models.db.cast(models.Inventory.value, models.db.Float).desc()).all()
	if fishes:
		for fish in fishes:
			fish_weight += int(float(fish.value.split(" ")[0]))
		fish_weight = fish_weight * 2
		
	
	old_level = pet.level
	choice = ""				
	answer = ""
	buttons = []
	
	
	req = reqData['userRequest']['utterance']
	
	
	
	if req.split(" ")[0] == '먹이주기':
				
		answer = "(+ω+)\n저는 \"" + pet_info.food + "\" 를 좋아해요❕\n경험치 "
		for i in range(0, int(pet.experience/10)):
			answer += "■"
			
		for i in range(0, 10-int(pet.experience/10)):
			answer += "□"
	
	elif req.split(" ")[0] == '한마리':
		fish_weight -= int(float(fishes[0].value.split(" ")[0]))*2
		if pet.experience + int(float(fishes[0].value.split(" ")[0]))*2 < 100:
			pet.experience += int(float(fishes[0].value.split(" ")[0]))*2
			answer = fishes[0].name + "를 줬다 👋\n경험치 "
			for i in range(0, int(pet.experience/10)):
				answer += "■"
			
			for i in range(0, 10-int(pet.experience/10)):
				answer += "□"
				
		else:
			pet.level += 1
			pet.experience = (pet.experience + int(float(fishes[0].value.split(" ")[0]))*2) - 100
		
		models.db.session.delete(fishes[0])
		models.db.session.commit()
		
	elif req.split(" ")[0] == '전부다':
		if pet.experience + fish_weight < 100:
			pet.experience += fish_weight
			answer = "물고기들을 줬다 👋\n경험치 "
			for i in range(0, int(pet.experience/10)):
				answer += "■"
			
			for i in range(0, 10-int(pet.experience/10)):
				answer += "□"
		
		else:
			pet.level += (pet.experience + fish_weight)//100
			pet.experience = (pet.experience + fish_weight) % 100
		
		for fish in fishes:	
			models.db.session.delete(fish)
		
		fish_weight = 0
		models.db.session.commit()		
	
	elif req.split(" ")[0] == '다음레벨까지':
		for fish in fishes:
			pet.experience += int(float(fish.value.split(" ")[0]))*2
			fish_weight -= int(float(fish.value.split(" ")[0]))*2
			models.db.session.delete(fish)
			if pet.experience >= 100: break
			
		pet.level += pet.experience//100
		pet.experience = pet.experience % 100
		models.db.session.commit()	
		
	elif req.split(" ")[0] == '만렙까지':
		for fish in fishes:
			pet.experience += int(float(fish.value.split(" ")[0]))*2
			fish_weight -= int(float(fish.value.split(" ")[0]))*2
			models.db.session.delete(fish)
			if pet.experience >= (10-pet.level)*100: break
			
		pet.level += pet.experience//100
		pet.experience = pet.experience % 100
		models.db.session.commit()	
	
	if old_level != pet.level:
		answer = pet.name + " 레벨업 " + str(old_level) + " ⇾ " + str(pet.level)  +" 🎉\n"
		
		for i in range(0, pet.level-old_level):
			choice, temp = level_up(pet.personality)
			if choice == '힘':
				pet.strength += 1
			elif choice == '지능':
				pet.intellect += 1
			elif choice == '체력':
				pet.health += 1
			else:
				pet.shild += 1
			
			answer += temp + "\n"
			models.db.session.commit()
		
	if pet.level < 10:	
					
		if fish_weight > 0:
			buttons.append({
					"blockId": "61275bd04738391855a634af",
					"action": "block",
					"label": "한마리 주기 🐟"
					})
		if fish_weight > 0 and fish_weight < (10-pet.level)*100 + (100-pet.experience):
			buttons.append({
					"blockId": "61275bd04738391855a634af",
					"action": "block",
					"label": "전부다 주기 🐟🐟"
					})
		
		if fish_weight >= 100 - pet.experience:
			buttons.append({
					"blockId": "61275bd04738391855a634af",
					"action": "block",
					"label": "다음레벨까지 🔥"
					})
	
		if fish_weight >= (10-pet.level)*100 + (100-pet.experience):
			buttons.append({
					"blockId": "61275bd04738391855a634af",
					"action": "block",
					"label": "만렙까지 🔥🔥"
					})
	buttons.append({
			"blockId": "61235128401b7e0601822e38",
			"action": "block",
			"label": "뒤로 👈️"
			})
	
	res = {
	"version": "2.0",
	"template": {
	"outputs": [
	{
	"simpleText": {
	"text": answer
	} 
	},
	],
	"quickReplies": buttons
	}
	}
					
	return res
	
def level_up(personality):
	personality_list = ['강인한', '창의적인', '듬직한', '끈기있는']
	stat_list = ['💪 힘', '🔮 지능', '🛡 방어력', '🩸 체력']
	number = random.randrange(0,100)
	
	if personality == '다재다능한':
		choice = random.choice(stat_list)
		
		
	else:
		if number < 65:
			choice = stat_list[personality_list.index(personality)]
		
		else:
			choice = random.choice(stat_list)
		
	answer = choice + "이 1 상승했어요"
	return choice.split(" ")[1], answer
		
