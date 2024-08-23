import random,Action
class Values:
	def __init__(self):#价值观/观念
		pass
class Personality:#性格
	def __init__(self):
		pass
class Intention:
	def __init__(self):#意图
		self.oldIntention=None
		self.EattingIntention=0#食欲
		self.EattingIntention_x=random.uniform(-0.1,0.1)#食欲修正
		self.EattingIntention_actions=['GET_SATIETY',[Action.Eat(),Action.pick_bush()]]
	def update(self,agent):
		#更新意图
		self.EattingIntention=1-agent.satiety/100+self.EattingIntention_x
		if self.EattingIntention<0:self.EattingIntention=0
		#根据进行最大意图进行决策
		intenDict={'EattingIntention':self.EattingIntention,'Error':-1}
		inten=max(intenDict,key=intenDict.get)
		if inten!=self.oldIntention or not agent.ActionList:
			agent.ActionList_close=[]
			agent.Goal=getattr(self,str(inten)+'_actions')[0]
			agent.ActionList=self.Goap(agent,getattr(self,str(inten)+'_actions')[1])
		#更新老意图
		self.oldIntention=inten
	def Goap(self,agent,actions):
		closeList=[]
		plan=[]
		TryNum=0
		while True:
			TryNum+=1
			if TryNum>len(actions):
				print('计划',plan[::-1])
				return plan[::-1]
			for action in actions:
				P=action.perconditionState(agent,plan)
				if action not in closeList and action.effectState(agent,plan) and P[0] and random.random()<action.preference:
					plan.append(action)
					closeList.append(action)
					if P[1]:#可以成立计划
						return plan[::-1]
class Mood:#心情
	def __init__(self):
		pass