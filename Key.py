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
		if event.type == pygame.KEYUP:
			if event.key==pygame.K_UP:
				self.m_u=False
			if event.key==pygame.K_DOWN:
				self.m_d=False
			if event.key==pygame.K_LEFT:
				self.m_l=False
			if event.key==pygame.K_RIGHT:
				self.m_r=False
		if event.type==pygame.MOUSEBUTTONDOWN:
			if event.button == 1 and self.tile_check:
				mouse_pos = pygame.mouse.get_pos()
				mouse_pos=list(mouse_pos)
				mouse_pos[0]-=self.tile_vx
				mouse_pos[1]-=self.tile_vy
				mouse_pos=mouse_pos[0],mouse_pos[1]
				for i in W.tile_list:
					for tile in i:
						if tile.rect.collidepoint(mouse_pos):
							self.tile_check=False
							self.is_tile_check=False
							self.tile=tile
			elif event.button == 1:
				mouse_pos = pygame.mouse.get_pos()
				mouse_pos=list(mouse_pos)
				mouse_pos[0]-=self.vx
				mouse_pos[1]-=self.vy
				mouse_pos=mouse_pos[0],mouse_pos[1]
				self.tile_obj=self.tile.tile_list[mouse_pos[0]//32][mouse_pos[1]//32]
			if self.tool_rect.collidepoint(event.pos):
				self.dragging=True
				self.offset_x = event.pos[0] - self.tool_rect.x
				self.offset_y = event.pos[1] - self.tool_rect.y
				self.tool_menu=True
				if self.is_tile_check:self.tile_check=False
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				self.dragging = False
		elif event.type == pygame.MOUSEMOTION:
			if self.dragging:
				self.tool_rect.x = event.pos[0] - self.offset_x
				self.tool_rect.y = event.pos[1] - self.offset_y
		
		
		
def key_act(self):
	if not self.tile_check:
		if self.m_u and self.vy<30:
			self.vy+=10
		if self.m_d and -self.vy+Setting.screen_size[1]<Setting.map_size[1]+30:
			self.vy-=10
		if self.m_l and self.vx<30:
			self.vx+=10
		if self.m_r and -self.vx+Setting.screen_size[0]<Setting.map_size[0]+30:
			self.vx-=10
	else:
		if self.m_u and self.tile_vy<30:
			self.tile_vy+=10
		if self.m_d and -self.tile_vy+Setting.screen_size[1]<Setting.map_size[1]+30:
			self.tile_vy-=10
		if self.m_l and self.tile_vx<30:
			self.tile_vx+=10
		if self.m_r and -self.tile_vx+Setting.screen_size[0]<Setting.map_size[0]+30:
			self.tile_vx-=10