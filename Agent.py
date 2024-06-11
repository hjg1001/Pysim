import Img,random,Method,Building
class Agent:
	def __init__(self,x,y,map_tile,O):
		self.surface=Img.images['agent']
		self.x,self.y=x,y#格点坐标
		self.map_tile=map_tile#所在大地图区块
		self.old_tile=map_tile.tile_list[x][y]
		self.tile=self.old_tile
		self.move_time=random.randint(10,19)#移动所需时间
		self.move_timer=0#移动计时
		self.road=[]
		self.target_x,self.target_y=None,None
		self.state=None
		self.action=None
		self.Organ=O
		self.Job=None
		#基本属性
		self.strength=random.randint(0,100)#力量
		self.intelligence=random.randint(0,100)#智力
		self.agility=random.randint(0,100)#敏捷
		self.max_hp=random.randint(50,250)#最大生命值
		#其他属性
		self.hp=self.max_hp
		self.satiety=100#饱食度
		#政策
		self.develop={'农业':10,'工业':0,'军事':2,'科研':1}
		S=sum(list(self.develop.values()))
		for name,value in self.develop.items():
			self.develop[name]=value/S
	def update(self,screen,U,font):
		if not U.pause:
			#更新地块
			self.update_tile()
			#更新状态
			if self.state=='move':self.move_state()
			#更新行为
			if self.Organ:
				if not self.Job:self.choose_job()
				if self.Job=='leader':self.Organ.update(self)
				elif self.Job=='农民':self.farmer_action()
				if self.satiety<40:self.eat()
			if random.randint(0,10000)>9800 and not self.state and not self.action:
				x,y=random.randint(0,49),random.randint(0,49)
				self.move(x,y)
		#更新表面
		if not U.is_tile_check and U.tile==self.map_tile:
			screen.blit(self.surface,(self.x*32+U.vx,self.y*32+U.vy))
			if self.road:self.draw_road(screen,U)
			if self.Organ:screen.blit(font.render(f'{self.Job}',False,(0,255,199)),(self.x*32+U.vx,self.y*32+U.vy-15))
		#自然变化
		self.update_self()
	def farmer_action(self):
		if not self.state and self.action=='farm':
			self.farm_state()
		else:
			if self.Organ.farm_list:
				for farm in self.Organ.farm_list:
					if farm.build_progress[0]<farm.build_progress[1]:
						if not farm.lock:
							self.farm(farm)#继续耕种
							farm.lock=self
							break
				if not self.action and len(self.Organ.farm_list)<self.Organ.farm_need:
					f=random.choice(self.Organ.farm_list)
					x,y=self.search_tile(f.x,f.y,'grass',1,'snow')#种新田
					if x:
						self.build_farm(x,y)
						print('种新田',self.x,self.y,'移动到',x,y)
					else:#不种田
						pass
			else:#建立组织第一个农场
				x,y=self.search_tile(self.x,self.y,'grass',50,'snow')
				if x:
					self.build_farm(x,y)
					print('种第一个田',self.x,self.y)
	def farm(self,farm):
		self.move(farm.x,farm.y)
		if self.state=='move' or (self.x==farm.x and self.y==farm.y):
			self.action='farm'
	def farm_state(self):
		Farm_obj=self.map_tile.tile_list[self.x][self.y].Building
		if Farm_obj.build_progress[0]<Farm_obj.build_progress[1]:
			Farm_obj.build_progress[0]+=self.strength*0.005
		else:
			self.action=None
			Farm_obj.lock=None
	def die(self):
		if self.Job!='leader':
			self.Organ.member.remove(self)
		else:#领导者死亡
			p=random.choice(self.Organ.member)
			self.Organ.leader=p
			p.Job='leader'
		self.map_tile.agent_list.remove(self)
		del self
	def search_tile(self,x,y,Type,num,Type2=True):
		T=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
		if num>50:num=50
		if self.map_tile.tile_list[x][y].Type in [Type,Type2]:
			if not self.map_tile.tile_list[x][y].Building:
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
				if x+i[0]>49 or y+i[1]>49:
					break
				if self.map_tile.tile_list[x+i[0]][y+i[1]].Type in [Type,Type2]:
					if not self.map_tile.tile_list[x+i[0]][y+i[1]].Building:
						return x+i[0],y+i[1]
			return None,None
	def build_farm(self,x,y):
		B=Building.Farm(x,y,self.Organ,self.map_tile)
		self.Organ.farm_list.append(B)
		self.map_tile.farm_list.append(B)
		self.map_tile.tile_list[x][y].Building=B
	def eat(self):
		if self.Organ.food>40:
			self.Organ.food-=40
			self.satiety+=40
		else:
			self.satiety+=self.Organ.food
			self.Organ.food=0
	def update_self(self):
		if self.satiety>0:self.satiety-=0.02
		elif self.satiety>100:self.satiety=100
		else:
			self.satiety=0
			self.hp-=0.03
		if self.hp<0:self.die()
	def update_tile(self):
		self.tile=self.map_tile.tile_list[self.x][self.y]
		if self.tile!=self.old_tile:
			self.old_tile.Obj=None
			self.old_tile.passability=0
		self.old_tile=self.tile
		self.tile.Obj=self
		self.tile.passability=None
	def choose_job(self):
		D=random.choices(list(self.Organ.develop.keys()),weights=list(self.Organ.develop.values()))
		if D[0]=='农业':
			self.Job='农民'
	def move(self,target_x,target_y):
		self.road=Method.bfs((self.x,self.y),(target_x,target_y),self.map_tile.tile_list)
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