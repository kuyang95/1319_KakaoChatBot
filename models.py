from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData


naming_convention = {
"ix": "ix_%(column_0_label)s",
"uq": "uq_%(table_name)s_%(column_0_name)s",
"ck": "ck_%(table_name)s_%(column_0_name)s",
"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
"pk": "pk_%(table_name)s"
	}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

class User(db.Model):
	
	__table_name__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String(32), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	attendanceDate = db.Column(db.String(30), nullable=True, default="0")
	loginPoint = db.Column(db.Integer, nullable=True, default=0)
	gold = db.Column(db.Integer, nullable=True, default=0)
	inventories = db.relationship("Inventory", backref='user')
	
	def __repr__(self):
		return '<User %r>' % self.userid
		
	def __init__(self, userid, password):
		self.userid = userid
		self.password = password

class ItemBook(db.Model):
	
	__table_name__ = 'item_book'
	id = db.Column(db.Integer, primary_key = True)
	category = db.Column(db.String(32), nullable=False)
	itemName = db.Column(db.String(50), nullable=False)
	descript = db.Column(db.String(100), nullable=False, default = None)
	spec = db.Column(db.String(100), nullable=True)
	buyPrice = db.Column(db.Integer, nullable=True, default = 0)
	sellPrice = db.Column(db.Integer, nullable=False)
	children = db.relationship("Inventory", backref="item_book")

	def __repr__(self):
		return '<ItemBook %r>' % self.id
	
	def __init__(self, category, itemName, descript, spec, buyPrice, sellPrice):
		self.category = category
		self.itemName = itemName
		self.descript = descript
		self.spec = spec
		self.buyPrice = buyPrice
		self.sellPrice = sellPrice
		
		
class Inventory(db.Model):
	__table_name__ = 'inventory'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=1)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	itemNo = db.Column(db.Integer, db.ForeignKey('item_book.id'))

	def __repr__(self):
		return '<Inventory %r>' % self.id
	
	def __init__(self, name, user_id, itemNo):
		self.name = name
		self.user_id = user_id
		self.itemNo = itemNo
		

class guestBook(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	writer = db.Column(db.String(32), nullable=False)
	input_text = db.Column(db.String(128), nullable= False)


	def __repr__(self):
		return '<guestBook %r>' % self.writer
		
	def __init__(self, writer, input_text):
		self.writer = writer
		self.input_text = input_text
