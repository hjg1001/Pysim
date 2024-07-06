import random,Name,Setting,Structure,pygame
class Nation:
	def __init__(self,SetTime):
		self.Name=Name.generate_nation_name()
		self.SetTime=SetTime
		self.Color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.City_list=[]
class City:
	def __init__(self,SetTime,nation,x,y):
		self.Name=Name.generate_city_name()
		self.x,self.y=x,y
		self.SetTime=SetTime
		self.Nation=nation
		self.ExpandTime=[0,10]
		self.MaxTile=300
		self.CityTile=[]
		self.VisitQueue=[]
		self.AgentList=[]
		self.ActionList={'farm':[0,0],'pick':[0,0]}#工作名额列表[已有/总共]
		self.BuildingList={'farm':[[],0]}
		self.ActionState=0#0-统计状态 1-招收状态
		self.Resource={'food':800}
		self.FarmList={}#种田者的工作安排{对象:[行为,X,Y,执行者]}
	def update(self,screen,U,Font,W):
		if not U.pause:
			#更新名额
			self.update_building_list()
			if self.AgentList:self.update_action_list()
			#规划
			if self.ActionState and len(self.FarmList)<self.ActionList['farm'][1]:
				self.set_farm_task(W)
			#扩张
			if len(self.CityTile)<self.MaxTile:
				self.ExpandTime[0]+=1
			if self.ExpandTime[0]>self.ExpandTime[1] and self.VisitQueue:
				num=self.try_expand(W,Setting.ExpandTile)
				if num:
					self.ExpandTime[1]+=num*3
					self.ExpandTime[0]=10
		#绘制
		self.draw_self(screen,U,Font)
	#--扩张 基于bfs
	def try_expand(self,W,num):
		visited=[]
		ExpandNum=[0,num]
		direction=[(0,1),(0,-1),(1,0),(-1,0)]
		Trying=True
		while Trying:
			tile=self.VisitQueue.pop()
			if not tile.City and tile.Terrain!='water':
				self.CityTile.append(tile)
				tile.City=self
				visited.append(tile)
				if tile in self.VisitQueue: self.VisitQueue.remove(tile)
				pygame.draw.rect(W.effect_surface,self.Nation.Color,(tile.x*32,tile.y*32,32,32))
				ExpandNum[0]+=1
			else:
				visited.append(tile)
				if tile in self.VisitQueue:self.VisitQueue.remove(tile)
			if tile.Terrain!='water' and (tile.City==self or not tile.City):
				for d in direction:
					nx,ny=tile.x+d[0],tile.y+d[1]
					if -1<nx<Setting.World_size[0] and -1<ny<Setting.World_size[1]:
						new_tile=W.World_map[nx][ny]
						if new_tile not in self.CityTile and new_tile not in visited:
							self.VisitQueue.append(new_tile)
						else:
							visited.append(new_tile)
			if ExpandNum[1]<ExpandNum[0]:Trying=False
			elif not self.VisitQueue:Trying=False
		return ExpandNum[0]
	#--下达命令
	def set_farm_task(self,W):#下令种田 单独分开
		for farm in self.BuildingList['farm'][0]:
			if farm not in list(self.FarmList.keys()) and farm.build_progress[0]<100:#种田
				self.FarmList[farm]=['continue_farm',farm.x,farm.y,None]
				return True
		if (not self.BuildingList['farm'][0] and self.FarmList)or (self.BuildingList['farm'][0] and len(self.BuildingList['farm'][0])<self.BuildingList['farm'][1]):#否则开新田
			if not self.BuildingList['farm'][0] and self.FarmList:fm=random.choice(list(self.FarmList.keys()))
			else:fm=random.choice(self.BuildingList['farm'][0])
			n=random.choice([[fm.x+1,fm.y],[fm.x-1,fm.y],[fm.x,fm.y+1],[fm.x,fm.y-1]])
			nx,ny=n[0],n[1]
			if -1<nx<Setting.World_size[0] and -1<ny<Setting.World_size[1] and not W.World_map[nx][ny].Structure and W.World_map[nx][ny].passability==0:#四向检索
				self.FarmList[Structure.Farm(nx,ny,self)]=['set_farm',nx,ny,None]
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
					if self.AgentList and self.Resource['food']:p=int((len(self.AgentList)*200)/self.Resource['food']*len(self.AgentList))
					else:p=15
					self.ActionList[action][1]=p if p>0 else 1
				elif action=='pick':
					self.ActionList[action][1]=1
		else:#招收完毕 重置工作名额
			for action in self.ActionList:
				self.ActionList[action][0]=0
	#--绘制
	def draw_self(self,screen,U,Font):
		screen.blit(Font.render(f'️{self.Name}'+['村','城'][0 if len(self.AgentList)<20 else 1]+str(self.Resource['food'])+'任务'+str(list(self.FarmList.values())),True,(254,150,57),self.Nation.Color),(self.x*32+U.vx,self.y*32+U.vy))
		if self.Nation.City_list[0]==self:screen.blit(Font.render(f'️{self.Nation.Name} 名额'+str(self.ActionList['farm'][0])+'/'+str(self.ActionList['farm'][1]),True,(0,0,0),self.Nation.Color),(self.x*32+U.vx,self.y*32+U.vy-20))