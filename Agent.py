import Img,Method,math,pygame,Setting,random,agentCore,Items
class Agent:
	def __init__(self,x,y,World):
		World.AgentList.append(self)
		self.x,self.y=x,y#屏幕坐标
		self.FloatX,self.FloatY=x,y
		self.target_x,self.target_y=None,None#屏幕坐标
		self.road=[]#格点坐标
		self.NewTile,self.OldTile=None,None
		self.Frame,self.FrameTime=0,0
		self.action,self.state=None,None
		self.AnimSpeed=3
		self.process=[0,0]
		self.AnimList={'None':[1,Img.images['agent_None']],'Move':[1,Img.images['agent_Move']]}
		self.MoveTime=[0,2]
		self.Flip=False
		self.Goal=None
		self.intention=agentCore.Intention()
		self.ActionList=[]
		self.ActionList_close=[]
		self.Inventory=[]
		self.debug=''
		#属性
		self.HP=[random.randint(100,150)]
		self.HP.append(self.HP[0])
		self.Speed=random.uniform(0.5,1.5)
		self.Strength=random.randint(0,100)#力量
		self.Intelligence=random.randint(0,100)#智力
		self.Agility=random.randint(0,100)#敏捷
		self.Perceptivity=random.randint(0,100)#感知
		#其他属性
		self.satiety=100#饱食度
		self.vision=40#视野
	def update(self,screen,World):
		self.update_tile(World)
	#属性更新
		self.satiety-=0.05
		if self.satiety>1:
			self.satiety-=0.01
		else:
			self.satiety=1
			self.HP[0]-=0.01
	#---主要更新
		self.intention.update(self)
		#行为更新
		if not self.action and self.ActionList:
			for act in self.ActionList:
				if act not in self.ActionList_close:
					self.action=act
					break
			if not self.action:#计划结束,为每个行动增加优先值
				for act in self.ActionList:
					if act.preference<0.9:act.preference+=random.uniform(0.01,0.03)
				self.ActionList,self.ActionList_close,self.Goal=[],[],None
		if self.action:self.action.run(self,World)
		#移动状态更新
		if self.state=='Move':
			self.MoveTime[0]+=2
		if self.MoveTime[0]>self.MoveTime[1]:
			self.MoveTime[0]=0
			self.moveState()
			self.x,self.y=int(self.FloatX),int(self.FloatY)
			self.AnimSpeed=self.Speed*1.4
		else:
			self.AnimSpeed=3
	#---绘制更新
		self.draw(screen)
	def update_tile(self,World):
		if not self.OldTile:self.OldTile=World.WorldMap[self.x//20][self.y//20]
		self.NewTile=World.WorldMap[self.x//20][self.y//20]
		if self.OldTile!=self.NewTile:
			self.OldTile.Unit.remove(self)
			self.OldTile=self.NewTile
		else:
			World.WorldMap[self.x//20][self.y//20].Unit.append(self)
	def draw(self,screen):#绘制
		self.animUpdate()
		Surface=self.AnimList[str(self.state)][1]
		if self.target_x and self.target_x<self.x:
			self.Flip=True
		if self.Flip:Surface=pygame.transform.flip(Surface,True,False)
		screen.blit(pygame.transform.scale(Surface,(self.AnimList[str(self.state)][1].get_width()*Setting.MapScale,self.AnimList[str(self.state)][1].get_height()*Setting.MapScale)),(self.x,self.y),(self.Frame*20*Setting.MapScale,0,20*Setting.MapScale,20*Setting.MapScale))
		if self.road:
			for num in range(len(self.road)):
				if len(self.road)>1 and num+1<len(self.road):
					pygame.draw.line(screen,(255,255,180),(self.road[num][0]*20,self.road[num][1]*20),(self.road[num+1][0]*20,self.road[num+1][1]*20))
				else:
					pygame.draw.line(screen,(255,255,180),(self.x,self.y),(self.road[0][0]*20,self.road[0][1]*20))
		#进度条
		if self.process[1]>self.process[0]:
			screen.blit(Img.images['process_1'],(self.x-2,self.y-5))
			screen.blit(Img.images['process_0'],(self.x-2,self.y-5),(0,0,int(self.process[0]/self.process[1]*30),2))
	def animUpdate(self):
		self.FrameTime+=self.AnimSpeed
		if self.FrameTime>60:
			self.FrameTime=0
			if self.Frame<self.AnimList[str(self.state)][0]:
				self.Frame+=1
			else:
				self.Frame=0
	#移动
	def move(self,targetx,targety,World):
		road=Method.bfs((self.x//20,self.y//20),(targetx,targety),World.WorldMap)
		if road:
			self.state='Move'
			self.road=road
	def moveState(self):
		if self.road and (not self.target_x or (self.FloatX==self.target_x and self.FloatY==self.target_y)):
			T=self.road.pop(0)
			self.target_x,self.target_y=T[0]*20,T[1]*20
		elif not self.road:
			self.state=None
			self.target_x,self.target_y=None,None
		if self.state=='Move':
			dx = self.target_x - self.FloatX
			dy = self.target_y - self.FloatY
			distance = math.sqrt(dx**2 + dy**2)
			if distance <= self.Speed:
				new_x = self.target_x
				new_y = self.target_y
			else:
				ratio = self.Speed / distance
				new_x = self.FloatX + dx * ratio
				new_y = self.FloatY + dy * ratio
			self.debug=(new_x,new_y),(self.FloatX,self.FloatY)
			self.FloatX,self.FloatY=new_x,new_y