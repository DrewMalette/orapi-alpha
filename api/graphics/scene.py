# media/input, mechanics, file handling

# i'm moving into an era where i'm replacing if statements
#  with boolean multiplication (where possible)
# tl;dr i'm replacing conditionals with boolean based calculations
# create the object within the Game object?
# create a Dialogue box then access it?
# then they need uids again

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
		
		for mob in self.live_mobs.values():	base_update(mob)
		self.game.terrain_renderer.update()
		
	def render(self):
	
		self.game.terrain_renderer.render()

