import random,Tile,pygame,Setting,Img,Structure,Organ,Agent,perlin_noise
import numpy as np
class World:
	def __init__(self):
		self.Agent_list=[]
		self.City_list=[]
		self.Nation_list=[]
		self.Building_list={'farm':[]}
		#其他属性
		self.Time=[0,0,0,0]#刻/天/月/年
#-----生成地图
		self.Noise=perlin_noise.PerlinNoise(3,Setting.Seed)
		self.surface=pygame.Surface((Setting.World_size[0]*32,Setting.World_size[1]*32))
		self.effect_surface=self.surface.copy()
		self.effect_surface.set_alpha(Setting.TerritoryAlpha)
		self.surface.fill((0,140,0))
		generate  =  np.vectorize(self.generate)
		self.World_map=generate(np.arange(Setting.World_size[0]),  np.arange(Setting.World_size[1]).reshape(-1,  1)).tolist()
		#其他操作
		if Setting.Draw_Tile_Edges:
			for x in range(0,Setting.World_size[0]):pygame.draw.line(self.surface,(0,0,0),(x*32,0),(x*32,Setting.World_size[0]*32))
			for y in range(0,Setting.World_size[1]):pygame.draw.line(self.surface,(0,0,0),(0,y*32),(Setting.World_size[1]*32,y*32))
		if Setting.Save_map_img:pygame.image.save(self.surface,'W.png')
		#debug
		for _ in range(Setting.AgentNum):
			T=self.World_map[1][19]
			T.Unit=Agent.Agent(2,19)
			self.Agent_list.append(T.Unit)
	def generate(self,y,x):#生成规则
			if self.Noise.noise([x/Setting.NoiseScale,y/Setting.NoiseScale])>0:
				T=Tile.Tile(x,y,'grass',0)
			else:
				T=Tile.Tile(x,y,'water',0)
				T.passability=None
				pygame.draw.rect(self.surface,(80,107,186),(x*32,y*32,32,32))
			if T.Terrain!='water' and random.random()<Setting.TreeProportion:
				T.Structure=Structure.Tree(x,y)
				T.passability=None
				self.surface.blit(Img.images['tree'],(x*32,y*32))
			elif T.Terrain!='water' and random.random()<Setting.BushProportion:
				T.Structure=Structure.Bush(x,y)
				self.surface.blit(Img.images['bush'],(x*32,y*32))
#			elif T.Terrain!='water' and Setting.AgentDensity>random.random() and Setting.AgentNum>len(self.Agent_list):
#				T.Unit=Agent.Agent(x,y)
#				self.Agent_list.append(T.Unit)
			return T
	def time_run(self):
		self.Time[0]+=30
		if self.Time[0]>500:
			self.Time[0]=0
			self.Time[1]+=1
		if self.Time[1]>31:
			self.Time[1]=0
			self.Time[2]+=1
		if self.Time[2]>12:
			self.Time[2]=0
			self.Time[3]+=1