import random,Tile,pygame,Setting,Img,Structure,Organ,Agent
import numpy as np
class World:
	def __init__(self):
		self.O_list=[]
		self.agent_list=[]
		self.farm_list=[]
		self.house_list=[]
#-----生成地图
		self.surface=pygame.Surface((Setting.World_size[0]*32,Setting.World_size[1]*32))
		self.surface.fill((0,140,0))
		generate  =  np.vectorize(self.generate)
		self.World_map=generate(np.arange(Setting.World_size[0]),  np.arange(Setting.World_size[1]).reshape(-1,  1)).tolist()
		if Setting.Draw_Tile_Edges:
			for x in range(0,Setting.World_size[0]):pygame.draw.line(self.surface,(0,0,0),(x*32,0),(x*32,Setting.World_size[0]*32))
			for y in range(0,Setting.World_size[1]):pygame.draw.line(self.surface,(0,0,0),(0,y*32),(Setting.World_size[1]*32,y*32))
		if Setting.Save_map_img:pygame.image.save(self.surface,'W.png')
		self.O_list.append(Organ.Organization(Agent.Agent(0,0,self,None,'leader')))#生成组织
		self.O_list[0].leader.Organ=self.O_list[0]
		while len(self.agent_list)<Setting.Agent_num:
			#生成智能体
			r_x,r_y=random.randint(10,25)+self.agent_list[0].x,random.randint(10,15)+self.agent_list[0].y
			T=self.World_map[r_x if Setting.World_size[0]>r_x>0 else 0][r_y if Setting.World_size[1]>r_y>0 else 0]
			if T.passability is not None and not T.Structure and not T.Unit:
				Agent.Agent(T.x,T.y,self,self.O_list[0])
	def generate(self,y,x):
			T=Tile.Tile(x,y,'grass',0)
			if random.random()>0.9:
				T.Structure=Structure.Tree(x,y)
				T.passability=None
				self.surface.blit(Img.images['tree'],(x*32,y*32))
			return T