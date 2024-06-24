class Tile:
	def __init__(self,x,y,T,Pass):
			self.x,self.y=x,y
			self.Terrain=T#地形
			self.passability=Pass#碰撞 None or int
			self.Unit=None#单位
			self.Structure=None#结构