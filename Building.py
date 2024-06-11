import Img
class Farm:
	def __init__(self,x,y,O,map_tile):
		self.x,self.y,self.O=x,y,O
		self.build_progress=[0,100]
		self.grow_progress=[0,100]
		self.surface=Img.images['farm0']
		self.map_tile=map_tile#所在大地图
		self.lock=None
	def update(self,screen,U,font):#建筑物通用更新
		if not U.pause:
			#更新工作者
			if self.lock and not self.lock.action=='farm' and self.O.leader.map_tile.tile_list[self.x][self.y].Obj!=self.lock:self.lock=None
			#更新田地
			if self.build_progress[0]>self.build_progress[1]:
				self.grow()
		#更新表面
		if not U.is_tile_check and U.tile==self.map_tile:
			if self.build_progress[1]>self.build_progress[0]:self.surface=Img.images['farm0']
			elif self.grow_progress[0]<20:self.surface=Img.images['farm1']
			elif 20<self.grow_progress[0]<40:self.surface=Img.images['farm2']
			elif 40<self.grow_progress[0]<60:self.surface=Img.images['farm3']
			elif 60<self.grow_progress[0]<80:self.surface=Img.images['farm4']
			else:self.surface=Img.images['farm4']
			screen.blit(self.surface,(self.x*32+U.vx,self.y*32+U.vy))
			screen.blit(font.render(f'{int(self.build_progress[0])}---{int(self.grow_progress[0])}',False,(0,255,199)),(self.x*32+U.vx,self.y*32+U.vy-25))
	def grow(self):
		if self.grow_progress[1]>self.grow_progress[0]:
			self.grow_progress[0]+=max(0.01,0.4-abs(24-self.O.leader.map_tile.Tem)*0.01)
		else:
			self.O.food+=10
			self.grow_progress[0]=0
			self.build_progress[0]=0