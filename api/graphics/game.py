import pygame

from . import mob
from . import scene
from . import terrain
from . import uidialogue
from . import uiselect
from . import utilities

from . import statetitle
from . import stategameplay

class Game:

	fps = 60
	display_size = (640,480)

	def __init__(self):
	
		pygame.display.set_caption("open rhombus")
		self.display = pygame.display.set_mode(self.display_size)
		self.fader = Fader(self, self.display.get_size())
		self.terrain_renderer = Terrain_Renderer("terrend", self)
		
		self.ui = {}
		self.ui["dialoguebox"] = uidialogue.UI_Dialogue("dialoguebox", self, (170,360), (300,100))
		self.ui["titleselect"] = uiselect.UI_Select("titleselect", self, (245,300), (150,54), ["Get Cucked", "Quit to Desktop"])
	
		self.controller = Keyboard(self)
		self.state = ""
		self.states = { "gameplay": stategameplay.State_Gameplay(self), "title": statetitle.State_Title(self) }
		
		self.clock = pygame.time.Clock()
		self.tick = 0
		
		self.player = None
		self.scene = None
		
		self.ui_font = pygame.font.Font(None, 24)
				
		# do some loading shit here
		self.title_music = pygame.mixer.Sound("content/sound/ccsong.ogg")
		#load_func(self)

	def switch_state(self, state_uid): # load and start
	
		self.state = state_uid
		self.states[self.state].start()

	def load_scene(self, uid, script_locals, terrain_filename, segment):
		
		self.scene = scene.Scene(uid, self, script_locals, segment)
		terrain.Terrain(terrain_filename, self, self.scene) # automatically sets self.scene.terrain to instance
		self.terrain_renderer.scene = self.scene
		self.terrain_renderer.following = self.player
		# assumes the tile is square
		self.terrain_renderer.tilesize = self.scene.terrain.tilewidth
		self.terrain_renderer.cols = int(self.terrain_renderer.w / self.scene.terrain.tilesize + 2)
		self.terrain_renderer.rows = int(self.terrain_renderer.h / self.scene.terrain.tilesize + 2)
		self.terrain_renderer.blank = pygame.Surface((self.scene.terrain.tilesize,self.scene.terrain.tilesize)).convert()
		self.terrain_renderer.blank.fill((0,0,0))
		
		#self.controller.flush()
		self.player.moving = False
		#self.sprites["player"].facing = "south" TODO put this somewhere else (like in a gamestate)
		self.terrain_renderer.update()		
	
	def main(self):
	
		self.running = True
		
		while self.running: self.update()
			
		pygame.quit()
		exit()

	def update(self):
	
		self.clock.tick(self.fps)
		self.tick = (self.tick + 1) % 4294967296
		pygame.event.pump()
		self.controller.update(pygame.key.get_pressed())
		self.states[self.state].update()
		pygame.display.flip()
		
	def render(self):
	
		#self.display.blit(self.camera.canvas,(0,0))
		#self.ui.blit(self.display)
		pass
			
class Controller:

	def __init__(self, game):
	
		self.game = game
		
		self.x_axis = self.y_axis = 0
		self.x_repeat = self.y_repeat = False
		self.x_pressed = self.y_pressed = False # USE THESE!!! Yes but actually no
		self.x_tick = self.y_tick = 0
		
		self.y_axis_sr = 0 # special repeat; delayed repeat
		self.y_axis_phase1 = 0 # for the first, and longer, delay
		self.y_axis_phase2 = 0 # for the constant and shorter delay
		
		self.as_pressed = False
		self.as_button = 0 # 'A' button single pulse
		self.ar_button = 0 # 'A' button repeating pulse; haven't coded this in yet
		
		self.exit = 0
		
	def flush(self):
	
		self.as_button = 0

class Keyboard(Controller):

	def __init__(self, game):
	
		Controller.__init__(self, game)
			
	def update(self, keys):
		
		self.x_axis = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] 
		self.y_axis = keys[pygame.K_DOWN] - keys[pygame.K_UP]
		self.y_axis_sr = 0
				
		self.as_button = 0
		self.ar_button = keys[pygame.K_RCTRL]
		
		self.exit = 0
		
		if self.x_axis != 0 and not self.x_pressed:
			self.x_tick = pygame.time.get_ticks()
			self.x_pressed = True
		elif self.x_axis == 0 and self.x_pressed:
			self.x_pressed = False
		self.x_repeat = self.x_pressed and (pygame.time.get_ticks() - self.x_tick >= 800)

		#if self.y_axis != 0 and not self.y_pressed:
		#	self.y_tick = pygame.time.get_ticks()
		#	self.y_pressed = True
		##elif self.y_axis == 0 and self.y_pressed:
		#	self.y_pressed = False
		#self.y_repeat = self.y_pressed and (pygame.time.get_ticks() - self.y_tick >= 800)

		if keys[pygame.K_RCTRL] == 1 and not self.as_pressed:
			self.as_pressed = True
			self.as_button = 1
		elif keys[pygame.K_RCTRL] == 0 and self.as_pressed:
			self.as_pressed = False

		if keys[pygame.K_ESCAPE] == 1:
			self.exit = 1

		if self.y_axis != 0 and not self.y_pressed:
			self.y_pressed = True
			self.y_tick = pygame.time.get_ticks()
			self.y_axis_sr = 1 # special repeat
			self.y_axis_phase1 = 1
		
		if self.y_pressed:
			if self.y_axis_phase1:
				if pygame.time.get_ticks() - self.y_tick >= 800:
					self.y_axis_phase2 = 1
					self.y_axis_phase1 = 0
					self.y_tick = pygame.time.get_ticks()
			elif self.y_axis_phase2:
				if pygame.time.get_ticks() - self.y_tick >= 100:
					self.y_axis_sr = 1
					self.y_tick = pygame.time.get_ticks()
				
		if self.y_axis == 0 and self.y_pressed:
			self.y_pressed = False

class Terrain_Renderer(pygame.Rect):

	def __init__(self, uid, game, x=0, y=0):
	
		self.uid = uid
		self.game = game
		w,h = self.game.display.get_size()
		pygame.Rect.__init__(self, (x,y,w,h))
		
		self.tilesize = 0 # TODO where does this get set?
		self.cols = 0
		self.rows = 0
		self.blank = None
		self.following = None
		self.scene = None
		
	def tile_prep(self, layer, col, row):

		x_offset = self.x % self.tilesize
		y_offset = self.y % self.tilesize

		c_index = int(self.x / self.tilesize + col)
		r_index = int(self.y / self.tilesize + row)
	
		index = self.scene.terrain.get_tile(layer, c_index, r_index)

		x = col * self.tilesize - x_offset
		y = row * self.tilesize - y_offset
		
		if index != "0":
			tile = self.scene.terrain.tileset[index]
			return (tile, x, y)
		else:			
			return ("0", x, y)
			
	def update(self):
	
		x,y = mob.get_centre(self.following)
		
		if x > self.w / 2:
			self.x = x - self.w / 2
		elif x <= self.w / 2:
			self.x = 0
		
		if y > self.h / 2:
			self.y = y - self.h / 2
		elif y <= self.h / 2:
			self.y = 0
	
		if self.x + self.w > self.scene.terrain.cols * self.tilesize:
			self.x = self.scene.terrain.cols * self.tilesize - self.w
		elif self.x < 0:
			self.x = 0
			
		if self.y + self.h > self.scene.terrain.rows * self.tilesize:
			self.y = self.scene.terrain.rows * self.tilesize - self.h
		elif self.y < 0:
			self.y = 0
				
	def render(self):
	
		for row in range(self.rows): # draw the bottom and middle tile layers
			for col in range(self.cols):
				x_offset = self.x % self.tilesize
				y_offset = self.y % self.tilesize

				c_index = int(self.x / self.tilesize + col)
				r_index = int(self.y / self.tilesize + row)
		
				bottom_i = self.scene.terrain.get_tile("bottom", c_index, r_index)
				middle_i = self.scene.terrain.get_tile("middle", c_index, r_index)

				c = col * self.tilesize - x_offset
				r = row * self.tilesize - y_offset
				
				if bottom_i != "0":
					bottom_t = self.scene.terrain.tileset[bottom_i]
					self.game.display.blit(bottom_t, (c,r))
				elif bottom_i == "0":
					self.game.display.blit(self.blank, (c,r))

				if middle_i != "0":
					middle_t = self.scene.terrain.tileset[middle_i]
					self.game.display.blit(middle_t, (c,r))

		#if self.scene.loot: # TODO merge this with sprites for the y_sort
		#	for loot in self.scene.loot.values():
		#		loot.render(self.game.display, x_offset = -self.x, y_offset = -self.y)

		if self.scene.live_mobs: # draw the sprites
			#for sprite in self.scene.sprites.values():
			for sprite in utilities.y_sort(self.scene.live_mobs.values()):
				mob.render(sprite, self.game.display, x_offset = -self.x, y_offset = -self.y)
		
		for row in range(self.rows): # draw the top layer
			for col in range(self.cols):
				tile, x, y = self.tile_prep("top", col, row)
				if tile != "0": self.game.display.blit(tile, (x, y))
				
class Fader: # TODO make a white version

	def __init__(self, game, size):
	
		self.game = game
		self.curtain = pygame.Surface(size)
		self.curtain.fill((0,0,0))
		self.opacity = 0
		self.curtain.set_alpha(self.opacity)
		
		self.speed = 0
		self.velocity = -self.speed
		self.faded_in = False # as in a cycle
		self.faded_out = False
		self.fading = False
	
	def fade_out(self, speed=6):
	
		self.speed = speed
		self.opacity = 0
		self.fading = True
		self.velocity = self.speed
		
	def fade_in(self, speed=6):
		
		self.speed = speed
		self.opacity = 255
		self.fading = True
		self.velocity = -self.speed
				
	def update(self):
	
		if self.faded_in: self.faded_in = False
		if self.faded_out: self.faded_out = False
		
		if self.fading:
		
			self.opacity += self.velocity
			
			if self.opacity <= 0:
				self.opacity = 0
				self.faded_in = True
			elif self.opacity >= 255:
				self.opacity = 255
				self.faded_out = True
			
			self.curtain.set_alpha(self.opacity)

			if self.faded_in or self.faded_out:
				self.fading = False

