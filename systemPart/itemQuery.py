import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import models

def changeAB(beforeName, afterName, uid, changeAnum):
	beforeItem = models.Inventory.query.filter(models.Inventory.user_id==uid, models.Inventory.name==beforeName).first()
	
	if beforeItem is None:
		return False
	
	afterItem = models.Inventory.query.filter(models.Inventory.user_id==uid, models.Inventory.name==afterName).first()
	afterItem_info = models.ItemBook.query.filter_by(itemName = afterName).first()
	
	if afterItem is None:
		if beforeItem.quantity > changeAnum:
			beforeItem.quantity -= changeAnum
			models.db.session.add(models.Inventory(afterName, uid, afterItem_info.id))
			
		elif beforeItem.quantity == changeAnum:
			models.db.session.add(models.Inventory(afterName, uid, afterItem_info.id))
			models.db.session.delete(beforeItem)
		
		else:
			return False
			
	else:
		if beforeItem.quantity > changeAnum:
			beforeItem.quantity -= changeAnum
			afterItem.quantity += 1
			
		elif beforeItem.quantity == changeAnum:
			models.db.session.delete(beforeItem)
			afterItem.quantity += 1
		
		else:
			return False
	
	models.db.session.commit()
	return True
	
def changeAGold(pickItem, uid, quantity):
	quantity = int(quantity)
	pickItem_info = models.ItemBook.query.filter_by(itemName = pickItem).first()
	pickItem = models.Inventory.query.filter(models.Inventory.user_id==uid, models.Inventory.name==pickItem).first()
	userProfile = models.User.query.filter_by(id = uid).first()
	
	if pickItem is None or pickItem_info is None:
		return False
	
	if pickItem.quantity < quantity:
		return False
	
	elif pickItem.quantity == quantity:
		userProfile.gold += pickItem_info.sellPrice * quantity
		models.db.session.delete(pickItem)
	
	else:
		userProfile.gold += pickItem_info.sellPrice * quantity
		pickItem.quantity -= quantity
		
	
	models.db.session.commit()
	
	return True
	
def addA(pickItem, uid, quantity):
	quantity = int(quantity)
	pickItem_info = models.ItemBook.query.filter_by(itemName = pickItem).first()
	pickItem = models.Inventory.query.filter(models.Inventory.user_id==uid, models.Inventory.name==pickItem).first()
	userProfile = models.User.query.filter_by(id = uid).first()
	
	if pickItem is None:
		models.db.session.add(models.Inventory(pickItem_info.itemName, userProfile.id, pickItem_info.id))
		
	else:
		pickItem.quantity += quantity
	
	
	models.db.session.commit()
	return True
