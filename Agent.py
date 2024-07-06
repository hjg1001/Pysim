import Img,random,Method,Structure,Setting,Organ,pygame
from collections import deque
class Agent:
	def __init__(self,x,y):
		self.surface=Img.images['agent']
		self.x,self.y=x,y#格点坐标
		self.old_tile=None
		self.tile=None
		self.move_time=random.randint(10,19)#移动所需时间
		self.move_timer=0#移动计时
		self.road=[]
		self.target_x,self.target_y=None,None
		self.state=None
		self.action=None
		self.city_action=None#分配到的行为
		self.Job=None
		self.Nation=None
		self.City=None
		self.work_building=None
		#基本属性
		self.strength=random.randint(10,100)#力量
		self.intelligence=random.randint(0,100)#智力
		self.agility=random.randint(0,100)#敏捷
		self.max_hp=random.randint(50,250)#最大生命值
		#其他属性
		self.hp=self.max_hp
		self.satiety=100#饱食度
	def update(self,screen,U,font,W):
		if not U.pause:
			self.update_tile(W)
			#更新行为
			if not self.action:
				#建立城市/国家
				if not self.Nation and self.get_tile_rect(self.x,self.y,4,W,'City',None):
					self.set_nation(W)
				#寻找最近城市加入
				elif W.Nation_list and not self.Nation:
					CityTile=random.choice(random.choice(W.City_list).CityTile)
					if CityTile.passability==0:
						self.move(CityTile.x,CityTile.y,W.World_map)
						if self.road:self.action='search_for_city'
				#获取工作
				if self.City and self.City.ActionState:
					for action in self.City.ActionList:
						if self.City.ActionList[action][1]>self.City.ActionList[action][0]:
							self.city_action=action
							self.City.ActionList[action][0]+=1
							break
				elif not self.city_action and not self.action and not self.state and self.City and random.randint(0,10000)>9990:
					T=random.choice(self.City.CityTile)
					self.move(T.x,T.y,W.World_map)#否则闲逛
			#更新行为至城市
			if self.City and self.action and self.City.ActionState==0:
				if self.city_action in self.City.ActionList.keys():
					self.City.ActionList[self.city_action][0]+=1
			#更新状态
			if self.state=='move':self.move_state()
			elif self.action=='search_for_city':#加入城市状态
				if self.tile.City:
					self.Nation=self.tile.City.Nation
					self.tile.City.AgentList.append(self)
					self.action=None
					self.City=self.tile.City
			elif self.city_action=='farm' and not self.action:#细分种田
				for farm in self.City.FarmList:
					if not self.City.FarmList[farm][3] or((self.City.FarmList[farm][3].x,self.City.FarmList[farm][3].y)!=(self.City.FarmList[farm][1],self.City.FarmList[farm][2])):
						if not self.City.FarmList[farm][3] or not self.City.FarmList[farm][3].road or (self.City.FarmList[farm][3].road[len(self.City.FarmList[farm][3].road)-1][0],self.City.FarmList[farm][3].road[len(self.City.FarmList[farm][3].road)-1][1])!=(self.City.FarmList[farm][1],self.City.FarmList[farm][2]):
							self.work_building=farm
							self.move(self.City.FarmList[farm][1],self.City.FarmList[farm][2],W.World_map)
							self.action=self.City.FarmList[farm][0]
							self.City.FarmList[farm][3]=self
							break
				if not self.action:self.city_action=None
			elif self.city_action=='pick' and not self.action:#采集
				T=random.choice(self.City.CityTile)
				if type(T.Structure).__name__=='Bush':
					self.move(T.x,T.y,W.World_map)
					if self.state=='move':
						self.action='pick_bush'
				if not self.action:self.city_action=None
			#细化行为下的状态
			if self.state=='move':pass
			elif self.action=='set_farm':#建新田
				W.World_map[self.x][self.y].Structure=self.work_building
				W.Building_list['farm'].append(self.work_building)
				self.City.BuildingList['farm'][0].append(self.work_building)
				self.action=None
				if self.work_building in list(self.City.FarmList.keys()):self.City.FarmList.pop(self.work_building)
				self.work_building=None
				self.city_action=None
			elif self.action=='continue_farm':#耕田
				self.work_building.build_progress[0]+=self.strength*0.01
				if self.work_building.build_progress[0]>self.work_building.build_progress[1]:
					self.action=None
					self.city_action=None
					if self.work_building in list(self.City.FarmList.keys()):self.City.FarmList.pop(self.work_building)
			elif self.action=='pick_bush':
				W.World_map[self.x][self.y].Structure.food-=1
				self.City.Resource['food']+=1
				if W.World_map[self.x][self.y].Structure.food<0:
					self.city_action=None
					self.action=None
					W.World_map[self.x][self.y].Structure=None
					pygame.draw.rect(W.surface,(0,140,0),(self.x*32+1,self.y*32+1,31,31))
			#更新自然状态
			if self.satiety>0:self.satiety-=0.06
			else:self.hp-=0.08
			if self.satiety<40 and self.City:
				if self.City.Resource['food']<40:
					self.satiety+=self.City.Resource['food']
					self.City.Resource['food']=0
				else:
					self.City.Resource['food']-=40
					self.satiety+=40
			if self.hp<0:self.die(W)
		#绘制
		self.draw_agent(screen,U,font)
		if self.road:self.draw_road(screen,U)
	#--方法
	def get_tile_rect(self,x,y,radius,W,info,need_info):#正方形全面检索(左至右)
		min_x=max(0,x-radius)
		max_x=min(Setting.World_size[0]-1,x+radius)
		min_y=max(0,y-radius)
		max_y=min(Setting.World_size[1]-1,y+radius)
		TileNum=[0,(max_x-min_x+1)*(max_y-min_y+1)]
		for nx in range(min_x,max_x+1):
			for ny in range(min_y,max_y+1):
				if getattr(W.World_map[nx][ny],info)==need_info:
					TileNum[0]+=1
		return TileNum[1]<=TileNum[0]
	#--死亡
	def die(self,W):
		if self.City:self.City.AgentList.remove(self)
		W.World_map[self.x][self.y].Unit=None
		W.Agent_list.remove(self)
		del self
	#--建立组织
	def set_nation(self,W):
		Nation=Organ.Nation(W.Time)
		W.Nation_list.append(Nation)
		self.set_city(W,Nation)
	def set_city(self,W,Nation):
		City=Organ.City(W.Time,Nation,self.x,self.y)
		CityTileSurface=pygame.Surface((32,32))
		CityTileSurface.fill(Nation.Color)
		radius=4
		for nx in range(max(0,self.x-radius),min(Setting.World_size[0]-1,self.x+radius)+1):
			for ny in range(max(0,self.y-radius),min(Setting.World_size[1]-1,self.y+radius)+1):
				setattr(W.World_map[nx][ny],'City',City)
				W.effect_surface.blit(CityTileSurface,(nx*32,ny*32))
				City.CityTile.append(W.World_map[nx][ny])
				City.VisitQueue.append(W.World_map[nx][ny])
		W.City_list.append(City)
		Nation.City_list.append(City)
	#--绘制
	def draw_road(self,screen,U):#绘制道路
		for x,y in self.road:
			if not self.action:screen.blit(Img.images['sign'],(x*32+U.vx,y*32+U.vy))
			else:screen.blit(Img.images['sign2'],(x*32+U.vx,y*32+U.vy))
	def draw_agent(self,screen,U,Font):
		screen.blit(self.surface,(self.x*32+U.vx,self.y*32+U.vy))
		screen.blit(Font.render(f'️{int(self.hp)}{self.city_action}/{self.action}--{self.state}',True,(195,5,9),(255,255,255)),(self.x*32+U.vx,self.y*32+U.vy-10))
	#--移动
	def update_tile(self,W):
		self.tile=W.World_map[self.x][self.y]
		self.tile.Unit=self
		if self.old_tile and self.tile!=self.old_tile:
			self.old_tile.Unit=None
		self.old_tile=self.tile
	def move(self,target_x,target_y,grid):#移动行为
		self.road=Method.bfs((self.x,self.y),(target_x,target_y),grid)
		if self.road:
			self.target_x,self.target_y=target_x,target_y
			self.state='move'
	def move_state(self):#移动状态
		self.move_timer+=1*(1+self.agility/100)
		dx=self.x-self.target_x
		dy=self.y-self.target_y
		if dx==0 and dy==0:
			self.state=None
			self.target_x,self.target_y=None,None
			self.move_timer=0
			self.road=[]
		elif self.move_timer>=self.move_time:
			if self.road:
				self.x,self.y=self.road[0]
				self.road.remove(self.road[0])
				self.move_timer=0
			else:
				self.state=None
				self.target_x,self.target_y=None,None
				self.move_timer=0