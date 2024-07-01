import Img,Setting
from random import choices
class Tree:
	def __init__(self,x,y):
		self.x,self.y=x,y
		self.hp=[100,100]
class Farm:
	def __init__(self,x,y,city):
		self.x,self.y=x,y
		self.city=city
		self.build_progress=[0,100]
		self.grow_progress=[0,100]
		self.surface=Img.images['farm0']
	def update(self,screen,U):#建筑物通用更新
		if not U.pause:
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
			self.city.Resource['food']+=38
			self.grow_progress[0]=0
			self.build_progress[0]=0