class Item:
	def __init__(self,name,Type,flag):
		self.name=name
		self.Type=Type
		self.flag=flag
	def use(self,user):#交给子类
		pass
class Food(Item):
	def __init__(self,name,satiety,flag=None):
		super().__init__(name,'Food',flag)
		self.satiety=satiety
	def use(self,user):
		user.satiety+=self.satiety
		user.Inventory.remove(self)
		del self