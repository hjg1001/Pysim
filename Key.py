import Setting,pygame
def control(self,event,W):
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_UP:
				self.m_u=True
			if event.key==pygame.K_DOWN:
				self.m_d=True
			if event.key==pygame.K_LEFT:
				self.m_l=True
			if event.key==pygame.K_RIGHT:
				self.m_r=True
		#松开按键
		elif event.type == pygame.KEYUP:
			if event.key==pygame.K_UP:
				self.m_u=False
			if event.key==pygame.K_DOWN:
				self.m_d=False
			if event.key==pygame.K_LEFT:
				self.m_l=False
			if event.key==pygame.K_RIGHT:
				self.m_r=False
		if event.type==pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if self.tool_rect.collidepoint(pos):
				self.tool_menu=True
		
		
def key_act(self):
	if self.m_u and self.vy<30:
		self.vy+=10
	if self.m_d and -self.vy+Setting.screen_size[1]<Setting.World_size[1]*32+30:
		self.vy-=10
	if self.m_l and self.vx<30:
		self.vx+=10
	if self.m_r and -self.vx+Setting.screen_size[0]<Setting.World_size[0]*32+30:
			self.vx-=10