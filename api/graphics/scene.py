# media/input, mechanics, file handling

# i'm moving into an era where i'm replacing if statements
#  with boolean multiplication (where possible)
# tl;dr i'm replacing conditionals with boolean based calculations
# create the object within the Game object?
# create a Dialogue box then access it?
# then they need uids again

from .mob import * # why do i need this?
			
class Scene:

	def __init__(self, uid, game, script_locals, segment):
	
		self.uid = uid
		self.game = game
		
		self.par_state = self.game.states["gameplay"]
		
		self.mobs = {}
		self.live_mobs = {}
		
		self.buildings = {}
		self.furniture = {}
		self.loot = {}
		
		self.script_locals = {}
		self.script_locals.update(script_locals)
		
		#self.segment = ""
		#self.segments = {}
		self.segment = segment
		#self.segments = {"ExpoDump": scene1_expo_dump, "Wait4Za": wait_for_pizza }

		self.terrain = None

	def add_mob(self, mob):
	
		self.mobs[mob.name] = mob
		
	def update(self):
		
		self.script_locals[self.segment](self)
	
		for mob in self.live_mobs.values():	base_update(mob)

#print(locals())
