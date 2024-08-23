import pygame,World,Setting,Agent
class EngineClass:
	def __init__(self):
		self.clock=pygame.time.Clock()
		self.Font1=pygame.font.Font('NotoSerifCJK-Regular.ttc',20)
		self.World=World.WorldClass()
		Agent.Agent(15*20,21*20,self.World)
		print(f'土地面积{self.World.Num[0]}/{self.World.Num[0]+self.World.Num[1]}')
	def Run(self,screen):
		while True:
			self.clock.tick(Setting.FPS)
			screen.fill((0,0,0))
			#世界更新
			for L in self.World.AreasList:
				for Area in L:
					if Area.x*10*20<Setting.ScreenSize[0] and Area.y*10*20<Setting.ScreenSize[1]:
						screen.blit(pygame.transform.scale(Area.surface,(200*Setting.MapScale,200*Setting.MapScale)),(Area.x*10*20,Area.y*10*20))
			for agent in self.World.AgentList:
				agent.update(screen,self.World)
			#渲染文字
			screen.blit(self.Font1.render('FPS'+str(int(self.clock.get_fps())),False,(250,250,250),(1,100,1)),(1,10))
			screen.blit(self.Font1.render('plan:'+str(self.World.AgentList[0].ActionList),False,(250,250,250),(1,100,1)),(1,50))
			screen.blit(self.Font1.render('action:'+str(self.World.AgentList[0].action),False,(250,250,250),(1,100,1)),(1,90))
			screen.blit(self.Font1.render('intention'+str(self.World.AgentList[0].intention.oldIntention),False,(250,250,250),(1,100,1)),(1,130))
			screen.blit(self.Font1.render('debug'+str(self.World.AgentList[0].debug),False,(255,200,250),(1,100,1)),(1,170))
			pygame.display.update()
def main():
	pygame.init()
	screen=pygame.display.set_mode((Setting.ScreenSize[0],Setting.ScreenSize[1]))
	Engine=EngineClass()
	Engine.Run(screen)
if __name__=='__main__':
	main()