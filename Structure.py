import Img
class Tree:
	def __init__(self,x,y):
		self.x,self.y=x,y
		self.hp=[100,100]
class House:
	def __init__(self,x,y,O):
		self.x,self.y,self.O=x,y,O
		self.build_progress=[0,100]
		self.people=[]
		self.max_people=2#这里指的是使用房屋的最大人数(睡觉工作等) 而非限制通过人数
		self.surface=Img.images['building']
		self.lock=[None,None,None,None]#四个位置
	def update(self,screen,U,font):#建筑物通用更新
		if not U.pause:
			#更新工作者
			for id,lock1 in enumerate(self.lock):
				if lock1:
					if not lock1.action=='build':self.lock[id]=None
					elif lock1.state=='move'and lock1.road and not (lock1.road[len(lock1.road)-1]==self.x and lock1.road[len(lock1.road)-1]==self.y):
						if not lock1.target_x==self.x and not lock1.target_y==self.y:
							if not lock1.x ==self.x and lock1.y==self.y:self.lock[id]=None
		#更新表面
		if self.build_progress[0]>self.build_progress[1]:self.surface=Img.images['house']
		screen.blit(self.surface,(self.x*32+U.vx,self.y*32+U.vy))
		screen.blit(font.render(f'{len(self.people)}',False,(0,255,199),(255,255,255)),(self.x*32+U.vx,self.y*32+U.vy-25))
class Farm:
	def __init__(self,x,y,O):
		self.x,self.y,self.O=x,y,O
		self.build_progress=[0,100]
		self.grow_progress=[0,100]
		self.surface=Img.images['farm0']
		self.lock=None
	def update(self,screen,U,font):#建筑物通用更新
		if not U.pause:
			#更新工作者
			if self.lock:
				if not self.lock.action=='farm':
					self.lock=None
				elif self.lock.state=='move'and self.lock.road and not (self.lock.road[len(self.lock.road)-1]==self.x and self.lock.road[len(self.lock.road)-1]==self.y):
					if not self.lock.target_x==self.x and not self.lock.target_y==self.y:
						if not self.lock.x ==self.x and self.lock.y==self.y:self.lock=None
			#更新田地
			if self.build_progress[0]>self.build_progress[1]:
				self.grow()
		#更新表面
		if self.build_progress[1]>self.build_progress[0]:self.surface=Img.images['farm0']
		elif self.grow_progress[0]<20:self.surface=Img.images['farm1']
		elif 20<self.grow_progress[0]<40:self.surface=Img.images['farm2']
		elif 40<self.grow_progress[0]<60:self.surface=Img.images['farm3']
		elif 60<self.grow_progress[0]<80:self.surface=Img.images['farm4']
		else:self.surface=Img.images['farm4']
		screen.blit(self.surface,(self.x*32+U.vx,self.y*32+U.vy))
	def grow(self):
		if self.grow_progress[1]>self.grow_progress[0]:
			self.grow_progress[0]+=0.3
		else:
			self.O.food+=38
			self.grow_progress[0]=0
			self.build_progress[0]=0