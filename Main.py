class UI:
	def __init__(self):
		self.m_u,self.m_d,self.m_l,self.m_r,self.pause=False,False,False,False,True
		self.tile_check=True
		self.tool_menu=False
		self.vx,self.vy=0,0
		self.tool_rect=pygame.Rect(30,10,50,50)
		self.dragging = False
		self.tile_obj=None
def Run():
	menu=pygame_menu.Menu(
        height=Setting.screen_size[1] * 0.3,
        theme=pygame_menu.themes.THEME_ORANGE,
        title='Tool menu',
        width=Setting.screen_size[0] * 0.4
    )
	menu.add.button('Quit',lambda: Exit(U))
	menu.add.selector('State',[('Pause', False), ('Run', True)],onchange=lambda x,y:pause(U))
	clock=pygame.time.Clock()
	while True:
		screen.fill((0,0,0))
		clock.tick(Setting.FPS)
		fps=int(clock.get_fps())
		events=pygame.event.get()
		for event in events:
			Key.control(U,event,W)
			if event.type == pygame.QUIT:
				break
		Key.key_act(U)
		#更新世界
		screen.blit(W.surface,(U.vx,U.vy))
		W.time_run()
		for L in W.Building_list.values():
			for building in L:
				building.update(screen,U)
		for agent in W.Agent_list:
			agent.update(screen,U,Font2,W)
		for city in W.City_list:
			city.update(screen,U,Font3,W)
		screen.blit(W.effect_surface,(U.vx,U.vy))
		#工具UI
		if U.tool_menu:menu.enable()
		else:menu.disable()
		if menu.is_enabled():
			menu.update(events)
			menu.draw(screen)
		screen.blit(Img.images['tool'],(30,10))
		#Debug
		screen.blit(Font.render(f'FPS:{fps}',True,(255,5,9),(0,0,0)),(0,60))
		screen.blit(Font.render(f'{W.Time[3]}年{W.Time[2]}月{W.Time[1]}天',True,(55,196,252),(255,255,255)),(0,100))
		pygame.display.update()
def pause(u):
	u.pause=not u.pause
def Exit(self):
	self.tool_menu=False
if __name__=='__main__':
	import time
	t0=time.time()
	import pygame,World,Key,Setting,pygame_menu,Img
	pygame.init()
	screen=pygame.display.set_mode(Setting.screen_size)
	W=World.World()
	U=UI()
	Font=pygame.font.Font('NotoSerifCJK-Regular.ttc',30)
	Font2=pygame.font.Font('NotoSerifCJK-Regular.ttc',10)
	Font3=pygame.font.Font('NotoSerifCJK-Regular.ttc',20)
	print('此次初始化用时',time.time()-t0)
	Run()