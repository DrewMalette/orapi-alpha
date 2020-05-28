# media/input, mechanics, file handling

from .mob import *
from .terrain import *

class Scene:

	def __init__(self, uid, game, terfile):
	
		self.uid = uid
		self.game = game
		
		self.mobs = {}
		self.live_mobs = {}
		
		self.buildings = {}
		self.furniture = {}
		self.loot = {}
		
		self.terrain = Terrain(terfile, game, self)

	def add_mob(self, mob):
	
		self.mobs[mob.name] = mob
		
	def update(self):
		
		for mob in self.live_mobs.values():	mob.base_update()
		self.game.renderer.update()
		
	def render(self):
	
		self.game.renderer.render()

