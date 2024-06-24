import Img,random,Method,Structure,Setting
class Agent:
	def __init__(self,x,y,W,O=None,Job=None):
		W.agent_list.append(self)
		if O and Job!='leader':
			O.member_list.append(self)
		self.surface=Img.images['agent']
		self.x,self.y=x,y#格点坐标
		self.old_tile=W.World_map[x][y]
		self.tile=self.old_tile
		self.move_time=random.randint(10,19)#移动所需时间
		self.move_timer=0#移动计时
		self.road=[]
		self.target_x,self.target_y=None,None
		self.state=None
		self.action=None
		self.Organ=O
		self.Job=Job
		#基本属性
		self.strength=random.randint(0,100)#力量
		self.intelligence=random.randint(0,100)#智力
		self.agility=random.randint(0,100)#敏捷
		self.max_hp=random.randint(50,250)#最大生命值
		#其他属性
		self.hp=self.max_hp
		self.satiety=100#饱食度
		#政策
		self.develop={'农业':random.randint(0,100),'工业':random.randint(0,100),'军事':random.randint(0,100),'科研':random.randint(0,100)}
		S=sum(list(self.develop.values()))
		for name,value in self.develop.items():
			self.develop[name]=value/S
	def update(self,screen,U,font,W):
		if not U.pause:
			grid=W.World_map
			#更新地块
			self.update_tile(grid)
			#更新状态
			if self.state=='move':self.move_state()
			#更新行为
			if self.Organ:
				if not self.Job:self.choose_job()
				if self.Job=='leader':self.Organ.update(self)
				elif self.Job=='农民':self.farmer_action(W)
				elif self.Job=='工人':self.worker_action(W)
				if self.satiety<40:self.eat()
			if random.randint(0,10000)>9990 and not self.state and not self.action:
				x,y=random.randint(0,49),random.randint(0,49)
				self.move(x,y,grid)
			#自然变化
			self.update_self(W)
		#更新表面
		if not type(W.World_map[self.x][self.y].Structure).__name__=='House':
			screen.blit(self.surface,(self.x*32+U.vx,self.y*32+U.vy))
			if self.road:self.draw_road(screen,U)
			if self.Organ:screen.blit(font.render(f'{self.Job}--{self.action}--{self.state}',False,(0,255,199),(255,255,255)),(self.x*32+U.vx,self.y*32+U.vy-25))
	def worker_action(self,W):
		if not self.state and self.action=='build':
			self.build_state(W.World_map)
		elif not self.state and 'set_'in str(self.action):
			self.setup_building_state(W)
		elif not self.action:
			if self.Organ.house_list:
				for house in self.Organ.house_list:
					if house.build_progress[0]<house.build_progress[1]:
						for Id,lock in enumerate(house.lock):
							if not lock:
								self.build(house,W.World_map,Id)#继续建造
								house.lock[Id]=self
								break
				if not self.action and len(self.Organ.house_list)<self.Organ.house_need:
					f=random.choice(self.Organ.house_list)
					x,y=self.search_tile(f.x,f.y,1,W.World_map,1)
					if x:
						self.setup_building(x,y,'house',W.World_map)
					else:#不建造房子
						pass
			else:#建立组织第一个房子
				x,y=self.search_tile(self.x,self.y,50,W.World_map,1)
				if x:	
					self.setup_building(x,y,'house',W.World_map)
	def setup_building(self,x,y,Type,grid):
		self.move(x,y,grid)
		if (self.state=='move' or self.road) or (self.x==x and self.y==y):
			if Type=='house':self.action='set_house'
	def setup_building_state(self,W):
		if self.action=='set_house':
			H=Structure.House(self.x,self.y,self.Organ)
			W.house_list.append(H)
			self.Organ.house_list.append(H)
			W.World_map[self.x][self.y].Structure=H
			W.World_map[self.x+1][self.y].Structure=H
			W.World_map[self.x][self.y+1].Structure=H
			W.World_map[self.x+1][self.y+1].Structure=H
		self.action=None
	def build(self,building,grid,Id):
		if Id==0:nx,ny=0,0
		elif Id==1:nx,ny=1,0
		elif Id==2:nx,ny=0,1
		else:nx,ny=1,1
		self.move(building.x+nx,building.y+ny,grid)
		if (self.state=='build' or self.road) or (self.x==building.x and self.y==building.y):
			self.action='build'
	def build_state(self,grid):
		Build_obj=grid[self.x][self.y].Structure
		if Build_obj and Build_obj.build_progress[0]<Build_obj.build_progress[1]:
			Build_obj.build_progress[0]+=self.strength*0.0008
		else:
			self.action=None
	def farmer_action(self,W):
		if not self.state and self.action=='farm':
			self.farm_state(W.World_map)
		else:
			if self.Organ.farm_list:
				for farm in self.Organ.farm_list:
					if farm.build_progress[0]<farm.build_progress[1]:
						if not farm.lock:
							self.farm(farm,W.World_map)#继续耕种
							farm.lock=self
							break
				if not self.action and len(self.Organ.farm_list)<self.Organ.farm_need:
					f=random.choice(self.Organ.farm_list)
					x,y=self.search_tile(f.x,f.y,1,W.World_map)#种新田
					if x:
						self.build_farm(x,y,W)
					else:#不种田
						pass
			else:#建立组织第一个农场
				x,y=self.search_tile(self.x,self.y,50,W.World_map)
				if x:
					self.build_farm(x,y,W)
	def farm(self,farm,grid):
		self.move(farm.x,farm.y,grid)
		if (self.state=='move' or self.road) or (self.x==farm.x and self.y==farm.y):
			self.action='farm'
	def farm_state(self,grid):
		Farm_obj=grid[self.x][self.y].Structure
		if Farm_obj and Farm_obj.build_progress[0]<Farm_obj.build_progress[1]:
			Farm_obj.build_progress[0]+=self.strength*0.01
		else:
			self.action=None
	def die(self,W):
		if self.Job!='leader':
			self.Organ.member_list.remove(self)
		else:#领导者死亡
			p=random.choice(self.Organ.member_list)
			self.Organ.leader=p
			p.Job='leader'
		W.agent_list.remove(self)
		del self
	def search_tile(self,x,y,num,grid,Type=0):#搜寻类型 0-无建筑物 1-四格无建筑物
		T=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
		if num>50:num=50
		if not grid[x][y].Structure:
			if Type==0:
				return x,y
			elif Type==1 and Setting.World_size[0]-1>x+1>0  and Setting.World_size[1]-1>y+1>0 and not grid[x+1][y].Structure and not grid[x][y+1].Structure and not grid[x+1][y+1].Structure:
				return x,y
		for _ in range(num):
			T[0][1]+=1
			T[1][1]-=1
			T[2][0]+=1
			T[3][0]-=1
			T[4][0]+=1
			T[4][1]+=1
			T[5][0]+=1
			T[5][1]-=1
			T[6][0]-=1
			T[6][1]+=1
			T[7][0]-=1
			T[7][1]-=1
			for i in T:
				if x+i[0]>49 or y+i[1]>49 or x+i[0]<0 or y+i[1]<0:
					break
				if not grid[x+i[0]][y+i[1]].Structure:
					if Type==0:
						return x+i[0],y+i[1]
					elif Type==1 and Setting.World_size[0]-1>x+i[0]+1>0 and Setting.World_size[1]-1>y+i[1]+1>0 and not grid[x+i[0]+1][y+i[1]].Structure and not grid[x+i[0]][y+i[1]+1].Structure and not grid[x+i[0]+1][y+i[1]+1].Structure:
						return x+i[0],y+i[1]
			return None,None
	def build_farm(self,x,y,W):
		B=self.Organ.Building_template['Farm'](x,y,self.Organ)
		self.Organ.farm_list.append(B)
		W.farm_list.append(B)
		W.World_map[x][y].Structure=B
	def eat(self):
		if self.Organ.food>40:
			self.Organ.food-=40
			self.satiety+=40
		else:
			self.satiety+=self.Organ.food
			self.Organ.food=0
	def update_self(self,W):
		if self.satiety>0:self.satiety-=0.02
		elif self.satiety>100:self.satiety=100
		else:
			self.satiety=0
			self.hp-=0.03
		if self.hp<0:self.die(W)
	def update_tile(self,grid):
		self.tile=grid[self.x][self.y]
		if self.tile!=self.old_tile:
			self.old_tile.Unit=None
			self.old_tile.passability=0
		self.old_tile=self.tile
		self.tile.Unit=self
		self.tile.passability=None
	def choose_job(self):
		D=random.choices(list(self.Organ.develop.keys()),weights=list(self.Organ.develop.values()))
		if D[0]=='农业':
			self.Job='农民'
		elif D[0]=='工业':
			self.Job='工人'
	def move(self,target_x,target_y,grid):
		self.road=Method.bfs((self.x,self.y),(target_x,target_y),grid)
		if self.road:
			self.target_x,self.target_y=target_x,target_y
			self.state='move'
	def draw_road(self,screen,U):
		for x,y in self.road:
			if not self.action:screen.blit(Img.images['sign'],(x*32+U.vx,y*32+U.vy))
			else:screen.blit(Img.images['sign2'],(x*32+U.vx,y*32+U.vy))
	def move_state(self):
		self.move_timer+=1
		dx=self.x-self.target_x
		dy=self.y-self.target_y
		if dx==0 and dy==0:
			self.state=None
			self.target_x,self.target_y=None,None
			self.move_timer=0
			self.road=[]
		elif self.move_timer==self.move_time:
			if self.road:
				self.x,self.y=self.road[0]
				self.road.remove(self.road[0])
				self.move_timer=0
			else:
				self.state=None
				self.target_x,self.target_y=None,None
				self.move_timer=0