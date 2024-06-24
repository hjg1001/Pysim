import random,Structure,Setting
class Organization:
	def __init__(self,leader,B={'Farm':lambda x,y,O:Structure.Farm(x,y,O),'House':lambda x,y,O:Structure.House(x,y,O)}):
		self.leader=leader
		self.member_list=[]
		self.type=None
		self.name=id(self.leader)
		self.develop=None
		self.food=Setting.food
		self.reform_time=2001#改革
		self.farm_list=[]
		self.farm_need=0
		self.house_list=[]
		self.house_need=[]
		self.Building_template=B#建筑模板
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
		self.house_need=int(len(self.member_list)/2)
		S=sum(list(self.develop.values()))
		for name,value in self.develop.items():
			self.develop[name]=value/S