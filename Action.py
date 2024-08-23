import random,Items,Img
from Method import search_tile
class Action:
	def __init__(self,name,condition,effect,preference):
		self.name=name
		self.init=False
		self.preference=preference#倾向(0-1)
		self.percondition=condition#前置条件
		self.effect=effect#后置效果
	def effectState(self,agent,plan):#后置效果是否满足
		return False#是否满足
	def perconditionState(self,agent,plan):#前置条件是否满足
		return False,False#是否满足,是否成立计划
	def run(self,agent,World):#交给子级
		pass
class Eat(Action):
	def __init__(self):
		self.food=None
		self.eatTime=[0,0]
		super().__init__('Eat','GET_FOOD','GET_SATIETY',1)
	def effectState(self,agent,plan):
		if agent.Goal=='GET_SATIETY':
			return True
	def perconditionState(self,agent,plan):
		for i in agent.Inventory:
			if i.Type=='Food':
				self.food=i
				return True,True
		return True,False
	def run(self,agent,World):
		if not self.init:
			self.init=True
			self.eatTime=[0,random.randint(100,150)]
			if not self.food:
				for i in agent.Inventory:
					if i.Type=='Food':
						self.food=i
						break
			if not self.food:
				self.food,self.init=None,False
				agent.ActionList_close.append(self)
				agent.action=None
		self.eatTime[0]+=1
		agent.process=self.eatTime
		if self.eatTime[0]>self.eatTime[1]:
			if self.food:self.food.use(agent)
			self.food,self.init=None,False
			agent.ActionList_close.append(self)
			agent.action=None
class pick_bush(Action):
	def __init__(self):
		self.pick_process=[0,0]
		self.bush_xy=0
		super().__init__('PickBush',None,'GET_FOOD',0.5)
	def effectState(self,agent,plan):
		if not plan:
			return False
		return plan[len(plan)-1].percondition==self.effect
	def perconditionState(self,agent,plan):
		return True,True
	def run(self,agent,World):
		if not self.init:
			self.pick_process=[0,200-agent.Perceptivity*0.8]
			xy=search_tile(World.WorldMap,'Structure','Type','Bush',agent.vision*2,agent.x//20,agent.y//20)
			self.bush_xy=xy
			if xy:
				agent.move(xy[0],xy[1],World)
			if not agent.state:
				for act in agent.ActionList:
					if act.preference>0.09:act.preference-=random.uniform(0.01,0.03)
				agent.ActionList,agent.ActionList_close,agent.Goal,agent.action=[],[],None,None
			else:
				self.init=True
		elif not agent.state:#到达目的地
			self.pick_process[0]+=1
			agent.process=self.pick_process
			if self.pick_process[0]>self.pick_process[1]:
				self.pick_process,self.init=None,False
				agent.ActionList_close.append(self)
				agent.action=None
				AreaX=self.bush_xy[0]//10
				AreaY=self.bush_xy[1]//10
				World.AreasList[AreaX][AreaY].surface.blit(Img.images['grass'],((self.bush_xy[0]-AreaX*10)*20+1,(self.bush_xy[1]-AreaY*10)*20+1),(random.randint(0,20),0,18,18))
				World.WorldMap[self.bush_xy[0]][self.bush_xy[1]].Structure=None
				for _ in range(1,2):agent.Inventory.append(Items.Food('浆果',random.randint(10,30)))