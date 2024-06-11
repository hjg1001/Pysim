import random,Tile,pygame,Setting,Organ
Terrain_type_list=[
'草地',
'平原',
'森林',
#'沙漠',
#'雪地',
#'雪林'
]
World_size=[1,2]
Tem=[30,-5]#最高温,最低温
Tem.append((Tem[0]-Tem[1])/(World_size[1]//2))#变化值
class World:
	def __init__(self):
		self.tile_list=[]
		self.O_list=[]
		self.surface=pygame.Surface((World_size[0]*200,World_size[1]*200))
		for x in range(World_size[0]):
			tem=Tem[1]
			self.tile_list.append([])
			if random.random()>0.65:No_desert=True
			else:No_desert=False
			for y in range(World_size[1]):
				if tem<=1:
						Type=random.choice(['雪地','雪林'])
				elif (not No_desert or tem>Tem[0]*0.9) and (tem>Tem[0]*0.8 or (tem>Tem[0]*0.65 and random.random()>0.8)):
					 Type='沙漠'
				else:
					Type=random.choice(Terrain_type_list)
				self.tile_list[x].append(Tile.Map_Tile(x,y,Type,int(tem)))
				self.surface.blit(pygame.transform.scale(self.tile_list[x][y].surface,(200,200)),(x*200,y*200))
				if Setting.Draw_Map_Edges:pygame.draw.rect(self.surface,(0,0,0),(x*200,y*200,200,200),2)
				if y<World_size[1]//2:#上半部分
					tem+=Tem[2]*1.1
				else:
					tem-=Tem[2]
		for i in self.tile_list:
			for t in i:
				if t.agent_list:
					o=Organ.Organization(t.agent_list[0],t.agent_list)
					self.O_list.append(o)
					t.agent_list[0].Organ=o
					t.agent_list[0].Job='leader'