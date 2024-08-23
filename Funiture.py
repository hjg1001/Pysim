class Door:
	def __init__(self,Type,state,lock):
		self.state=state#开关状态 0关1开
		self.lock=lock if not self.state else False#上锁状态
		if Type==0:
			self.surface=[]