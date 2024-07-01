import random,Name,Setting,Structure
class Nation:
	def __init__(self,SetTime):
		self.Name=Name.generate_nation_name()
		print(self.Name)
		self.SetTime=SetTime
		self.Color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.City_list=[]
class City:
	def __init__(self,SetTime,nation,x,y):
		self.Name=Name.generate_city_name()
		self.x,self.y=x,y
		self.SetTime=SetTime
		self.Nation=nation
		self.CityTile=[]
		self.AgentList=[]
		self.ActionList={'farm':[0,0]}#工作名额列表[已有/总共]
		self.BuildingList={'farm':[[],0]}
		self.ActionState=0#0-统计状态 1-招收状态
		self.Resource={'food':0}
		self.FarmList={}#种田者的工作安排{对象:[行为,X,Y,执行者]}
	def update(self,screen,U,Font,W):
		#更新名额
		self.update_building_list()
		if self.AgentList:self.update_action_list()
		#规划
		if self.ActionState and len(self.FarmList)<self.ActionList['farm'][1]:
			self.set_farm_task(W)
		#绘制
		self.draw_self(screen,U,Font)
	#--下达命令
	def set_farm_task(self,W):#下令种田 单独分开
		for farm in self.BuildingList['farm'][0]:
			if farm not in self.FarmList.keys() and farm.build_progress[0]<100:#种田
				self.FarmList[farm]=['continue_farm',farm.x,farm.y,None]
				return True
		if self.BuildingList['farm'][0] and len(self.BuildingList['farm'][0])<self.BuildingList['farm'][1]:#否则开新田
			fm=random.choice(self.BuildingList['farm'][0])
			nx,ny=random.choice([max(0,fm.x-1),min(Setting.World_size[0],fm.x+1)]),random.choice([max(0,fm.y-1),min(Setting.World_size[0],fm.y+1)])
			if (nx!=fm.x or ny!=fm.y) and not W.World_map[nx][ny].Structure and W.World_map[nx][ny].passability:#八向检索
				self.FarmList[Structure.Farm(nx,ny,self)]=['set_farm',fm.x,fm.y,None]
		elif len(self.BuildingList['farm'][0])<self.BuildingList['farm'][1]:#否则开一个全新的田
			T=random.choice(self.CityTile)
			if T.passability==0 and not T.Structure:
				self.FarmList[Structure.Farm(T.x,T.y,self)]=['set_farm',T.x,T.y,None]
	#--更新列表
	def update_building_list(self):
		if self.ActionState:
			for building in self.BuildingList:
				if building=='farm':self.BuildingList['farm'][1]=self.ActionList['farm'][1]
	def update_action_list(self):
		if self.ActionState:self.ActionState=0
		else:self.ActionState=1
		if self.ActionState:#自发统计完毕 重新计算总工作名额 以备下一回合取工作
			for action in self.ActionList:
				if action=='farm':
					p=int((1-self.Resource['food']/len((self.AgentList)*100))*len(self.AgentList))
					self.ActionList[action][1]=p if p>0 else 1
		else:#招收完毕 重置工作名额
			for action in self.ActionList:
				self.ActionList[action][0]=0
	#--绘制
	def draw_self(self,screen,U,Font):
		screen.blit(Font.render(f'️{self.Name}'+['村','城'][0 if len(self.AgentList)<20 else 1],True,(254,150,57),self.Nation.Color),(self.x*32+U.vx,self.y*32+U.vy))
		if self.Nation.City_list[0]==self:screen.blit(Font.render(f'️{self.Nation.Name} 种田名额'+str(self.ActionList['farm'][0])+'/'+str(self.ActionList['farm'][1]),True,(0,0,0),self.Nation.Color),(self.x*32+U.vx,self.y*32+U.vy-20))