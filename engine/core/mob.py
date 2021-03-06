
import pygame
#from .mechanics import StatBlock
from . import utilities

heading = { (0,-1): "north", (0,1): "south", (-1,0): "west", (1,0): "east",
			(-1,-1): "north", (1,1): "south", (-1,1): "west", (1,-1): "east" }

north_rect = lambda mob: (mob.x, mob.y - mob.h)
south_rect = lambda mob: (mob.x, mob.y + mob.h)
west_rect = lambda mob: (mob.x - mob.w, mob.y)
east_rect = lambda mob: (mob.x + mob.w, mob.y)

talk_rect = { "north": north_rect, "south": south_rect, "west": west_rect, "east": east_rect }

class Mob(pygame.Rect):

	pattern = [0,1,0,2]
	facings = { "south": 0, "north": 1, "east": 2, "west": 3 }

	def __init__(self, game, filename, name):
	
		self.game = game
	
		data = utilities.load_mob_sprite(filename)
		pygame.Rect.__init__(self, data["rect"])
		self.cols = data["cols"]
		self.rows = data["rows"]
		self.cells = data["cells"]
		self.x_offset, self.y_offset = data["offsets"]
				
		self.moving = False
		self.facing = "south"
		self.frame = 0
		self.scene = None
		self.speed = 2

		self.alive = True # going to StatBlock?
		self.dying = False
		self.opacity = 255
		
		self.talk_rect = pygame.Rect(0,0,12,12)
		
	def spawn(self):
	
		self.scene.live_mobs[self.name] = self
	
	def kill(self):
	
		del self.scene.live_mobs[self.name]
		
	def place(self, col, row):
		
		self.x = col * self.scene.tilesize + (self.scene.tilesize - self.w) / 2
		self.y = row * self.scene.tilesize + (self.scene.tilesize - self.h) - 4

	def get_cell(self, col, row):

		if (col >= 0 and col < self.cols) and (row >= 0 and row < self.rows):
			return self.cells[self.cols*row+col]
		else:
			print("col or row out of sprite's bounds")
			pygame.quit()
			exit()

	def move(self, x_axis, y_axis):

		x = (not self.collision(x_axis * self.speed, 0)) * (x_axis * self.speed)
		y = (not self.collision(0, y_axis * self.speed)) * (y_axis * self.speed)
		self.move_ip(x*self.moving, y*self.moving)
		if x_axis != 0 or y_axis != 0: self.facing = heading[(x_axis,y_axis)]

	def collision(self, x_axis, y_axis):

		for c in range(4):
			xm = ((self.x + x_axis * self.speed) + (c % 2) * self.w)
			ym = ((self.y + y_axis * self.speed) + int(c / 2) * self.h)

			col = int(xm / self.scene.tilesize) # is this slow?
			row = int(ym / self.scene.tilesize)

			if self.scene.get_tile("collide", col, row) != "0":
				return True

		for sprite in self.scene.live_mobs.values():
			if sprite is not self:
				xm = self.speed * x_axis + self.x
				ym = self.speed * y_axis + self.y
				if sprite.colliderect((xm, ym, self.w, self.h)):
					return True
		return False
		
	def base_update(self):

		# self.statblock.upkeep() TODO move this to a derivative class
		self.moving = bool(self.game.controller.x_axis or self.game.controller.y_axis)	
		self.frame += self.moving & (self.game.tick % 12 == 0) * 1
		self.frame = self.frame % len(self.pattern) * self.moving
		
	def update(self): # overridden by classes derived

		self.base_update()
		
	def render(self, surface, x_offset=0, y_offset=0):

		x = (self.x - self.x_offset) + x_offset
		y = (self.y - self.y_offset) + y_offset
		frame = self.pattern[self.frame]
		facing = self.facings[self.facing]
		surface.blit(self.get_cell(frame, facing), (x,y))
		
