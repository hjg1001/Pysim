import Img,Setting,random,pygame,Structure
from Method import generate_noise
import numpy as np
class Tile:
	def __init__(self,x,y,Terrain,Pass):
		self.x,self.y=x,y
		self.Structure=None
		self.Unit=[]
		self.Terrain=Terrain
		self.Funiture=None
		self.Pass=Pass
class Area:
	def __init__(self,x,y):
		self.water=0
		self.tree=0
		self.x,self.y=x,y
		self.surface=pygame.Surface((10*20,10*20))
class WorldClass:
	def __init__(self):
		self.AreasList=[]#标准[x][y]
		self.AgentList=[]
		#---生成地图
		self.Num=[0,0]
		self.Noise=generate_noise([Setting.WorldSize[0],Setting.WorldSize[1]],[2,2])#平滑噪声
		self.Noise2=generate_noise([Setting.WorldSize[0],Setting.WorldSize[1]],[2,5])#碎片噪声1
		self.Noise3=generate_noise([Setting.WorldSize[0],Setting.WorldSize[1]],[5,2])#碎片噪声2
		self.Noise4=generate_noise([Setting.WorldSize[0],Setting.WorldSize[1]],[5,5])#自然噪声
		generate  =  np.vectorize(self.generate) 
		self.WorldMap=generate(np.arange(Setting.WorldSize[0]),  np.arange(Setting.WorldSize[1]).reshape(-1,  1)).tolist()
		#---划线
		if Setting.DrawTile or Setting.DrawArea:
			for l in self.AreasList:
				for a in l:
					if Setting.DrawArea:pygame.draw.rect(a.surface,(255,0,0),(0,0,10*20,10*20),1)
					if Setting.DrawTile:
						for Y in range(10):pygame.draw.line(a.surface,(0,0,0),(0,Y*20),(10*20,Y*20))
						for X in range(10):pygame.draw.line(a.surface,(0,0,0),(X*20,0),(X*20,10*20))
					#同时生成区域内容
	def generate(self,y,x):
		#添加区块
		AreaX=x//10
		AreaY=y//10
		if len(self.AreasList)<=AreaX:
			self.AreasList.append([])
		if len(self.AreasList[AreaX])<=AreaY:
			self.AreasList[AreaX].append(Area(AreaX,AreaY))
		#区块中添加地块
		NoiseValue=self.Noise[x][y]+self.Noise2[x][y]*Setting.WorldNoise[0]+self.Noise3[x][y]*Setting.WorldNoise[1]
		if NoiseValue>228:
			T=Tile(x,y,'grass',True)
			self.Num[0]+=1
			self.AreasList[AreaX][AreaY].surface.blit(Img.images['grass'],((x-AreaX*10)*20,(y-AreaY*10)*20),(random.randint(0,20),0,20,20))
		elif 220<NoiseValue<=228:
			T=Tile(x,y,'sand',True)
			self.Num[0]+=1
			self.AreasList[AreaX][AreaY].surface.blit(Img.images['sand'],((x-AreaX*10)*20,(y-AreaY*10)*20),(random.randint(0,20),0,20,20))
		else:
			self.AreasList[AreaX][AreaY].water+=1
			T=Tile(x,y,'water',False)
			self.Num[1]+=1
			self.AreasList[AreaX][AreaY].surface.blit(Img.images['water'],((x-AreaX*10)*20,(y-AreaY*10)*20),(random.randint(0,20),0,20,20))
		#生成资源
		if 180>self.Noise4[x][y]>100 and random.random()>0.6 and T.Terrain=='grass':
			T.Structure=Structure.Tree(x,y)
			T.Pass=False
			self.AreasList[AreaX][AreaY].tree+=1
			self.AreasList[AreaX][AreaY].surface.blit(Img.images['tree'],((x-AreaX*10)*20,(y-AreaY*10)*20))
		elif 100>self.Noise4[x][y]>80 and random.random()>0.8 and T.Terrain=='grass':
			T.Structure=Structure.Bush(x,y)
			T.Pass=True
			self.AreasList[AreaX][AreaY].surface.blit(Img.images['bush'],((x-AreaX*10)*20,(y-AreaY*10)*20))
		return T