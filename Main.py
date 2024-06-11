class UI:
	def __init__(self,W):
		self.m_u,self.m_d,self.m_l,self.m_r,self.pause=False,False,False,False,True
		self.vx,self.vy=screen.get_rect().center
		self.vx-=25*32
		self.vy-=25*32
		self.tile_check=True
		self.tile_vx,self.tile_vy=screen.get_rect().center#大地图偏移
		self.tile_vx-=len(W.tile_list)*100
		self.tile_vy-=len(W.tile_list[0])*100
		self.tile=None
		self.is_tile_check=True
		self.tool_menu=False
		self.tool_rect=pygame.Rect(30,10,35,35)
		self.dragging = False
		self.offset_x = 0
		self.offset_y = 0
		self.tile_obj=None
def Run():
	menu=pygame_menu.Menu(
        height=Setting.screen_size[1] * 0.3,
        theme=pygame_menu.themes.THEME_ORANGE,
        title='Tool menu',
        width=Setting.screen_size[0] * 0.4
    )
	menu.add.button('Return Global Map',lambda:cancel_check(U))
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
		if U.tile_check:screen.blit(W.surface,(U.tile_vx,U.tile_vy))
		elif U.tile:screen.blit(U.tile.surface,(U.vx,U.vy))
		#更新世界
		for X in W.tile_list:
			for area in X:
				for farm in area.farm_list:
					farm.update(screen,U,Font2)
				for agent in area.agent_list:
					agent.update(screen,U,Font2)
		#工具UI
		if U.tool_menu:menu.enable()
		else:menu.disable()
		if menu.is_enabled():
			menu.update(events)
			menu.draw(screen)
		screen.blit(Img.images['tool'],U.tool_rect)
	#	if U.tile_obj:a,b=U.tile_obj.Type,U.tile_obj.passability
	#	else:a,b=0,0
		if U.tile:c=U.tile.agent_list[0].satiety
		else:c=0
		if U.tile and W.O_list[0].develop:d=list(W.O_list[0].develop.items())[0][1]
		else:d=0
		screen.blit(Font.render(f'FPS:{fps}--{c}--{d}--{W.O_list[0].reform_time}',True,(255,5,9)),(0,60))
		pygame.display.update()
def cancel_check(self):
	self.tile_check=True
	self.is_tile_check=True
	Exit(self)
def pause(u):
	u.pause=not u.pause
def Exit(self):
	if self.is_tile_check:self.tile_check=True
	self.tool_menu=False
if __name__=='__main__':
	import time
	t0=time.time()
	import pygame,World,Key,Setting,pygame_menu,Img
	pygame.init()
	screen=pygame.display.set_mode(Setting.screen_size)
	W=World.World()
	pygame.image.save(W.surface,'W.png')
	U=UI(W)
	Font=pygame.font.Font('NotoSerifCJK-Regular.ttc',30)
	Font2=pygame.font.Font('NotoSerifCJK-Regular.ttc',20)
	print('此次初始化用时',time.time()-t0)
	Run()