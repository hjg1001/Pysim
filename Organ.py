import random
class Organization:
	def __init__(self,leader,init_list=None,food=0):
		self.leader=leader
		self.member_list=[]
		self.type=None
		self.name=id(self.leader)
		self.develop=None
		self.food=food
		self.reform_time=2001#改革
		self.farm_list=[]
		self.farm_need=[]
		if init_list:#程序初期建立的组织
			for p in init_list:#强制把开局的智能体全部纳入组织
				if not p.Organ:
					p.Organ=self
					self.member_list.append(p)
	def update(self,leader):#运行组织
		#--改革
		if not self.develop:self.develop=leader.develop
		self.reform_time+=1
		if self.reform_time>2000:
			self.reform_time=0
			self.updata_develop()
	def updata_develop(self):#改革 动态调整发展优先级
		self.develop['农业']=(100+len(self.member_list)*10)/(self.food+1)
		self.farm_need=len(self.member_list)+random.randint(-1,6)
		if self.leader.map_tile.terrain_type=='沙漠':self.develop['农业']=0
		S=sum(list(self.develop.values()))
		for name,value in self.develop.items():
			self.develop[name]=value/S