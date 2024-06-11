import random,pygame,Img,Setting,Agent
import Method
class Tile:
	def __init__(self,x,y,Type,Pass,obj):
			self.x,self.y=x,y
			self.Type=Type
			self.passability=Pass#碰撞
			self.Obj=obj#地块上的对象(占位者)
			self.Building=None
class Map_Tile:
	def __init__(self,x,y,Type,tem):
		self.x,self.y=x,y
		self.terrain_type=Type
		self.surface=pygame.Surface((50*32,50*32))
		self.rect=pygame.Surface((200,200)).get_rect()
		self.rect.topleft=(x*200,y*200)
		self.tile_list=[]
		noise=Method.generate_noise([50,50],[5,5])
		#地块占比
		self.water_proportion=0
		self.sand_proportion=0
		self.snow_proportion=0
		#其他占比
		self.tree_proportion=0
		#其他属性
		self.Tem=tem
		#区块对象
		self.agent_list=[]
		self.farm_list=[]
		if self.terrain_type=='草地':
			self.water_proportion=40+random.randint(-10,10)
			self.tree_proportion=random.random()*0.09
		elif self.terrain_type=='平原':
			self.water_proportion=50+random.randint(-10,10)
			self.tree_proportion=random.random()*0.09
		elif self.terrain_type=='森林':
			self.water_proportion=90+random.randint(-10,10)
			self.tree_proportion=0.5+(random.random()-random.random())*0.9
		elif self.terrain_type=='沙漠':
			self.water_proportion=0
			self.sand_proportion=1000
			self.tree_proportion=0.001
		elif self.terrain_type=='雪地':
			self.water_proportion=80+random.randint(-10,10)
			self.snow_proportion=1000
			self.tree_proportion=random.random()*0.09
		elif self.terrain_type=='雪林':
			self.water_proportion=90+random.randint(-10,10)
			self.snow_proportion=1000
			self.tree_proportion=0.9+(random.random()-random.random())*0.1
		for x in range(50):
			self.tile_list.append([])
			for y in range(50):
				W=noise[x][y]
				if W<self.water_proportion:
					self.tile_list[x].append(Tile(x,y,'water',100,None))
					self.surface.blit(Img.images['water'],(x*32,y*32))
					self.tile_list[x][y].passability=None
				elif W<self.sand_proportion:
					self.tile_list[x].append(Tile(x,y,'sand',0,None))
					self.surface.blit(Img.images['sand'],(x*32,y*32),(random.randint(50,255-50),0,32,32))
				elif W<self.snow_proportion:
					self.surface.blit(Img.images['snow'],(x*32,y*32),(random.randint(50,255-50),0,32,32))
					self.tile_list[x].append(Tile(x,y,'snow',0,None))
				else:
					self.surface.blit(Img.images['grass'],(x*32,y*32),(random.randint(50,255-50),0,32,32))
					self.tile_list[x].append(Tile(x,y,'grass',0,None))
				#其他
				if random.random()<self.tree_proportion and self.tile_list[x][y].Type!='water' and random.random()>0.6:
					self.tile_list[x][y].Obj='Tree'
					self.tile_list[x][y].passability=None
					self.surface.blit(Img.images['tree'],(x*32,y*32))
				elif W>random.random()*Setting.Agent_sparse and self.tile_list[x][y].Type!='water':
					A=Agent.Agent(x,y,self,None)
					self.tile_list[x][y].Obj=A
					self.agent_list.append(A)
				if Setting.Draw_Tile_Edges:pygame.draw.rect(self.surface,(0,0,100),(x*32,y*32,32,32),1)
		print(self.terrain_type,self.agent_list)