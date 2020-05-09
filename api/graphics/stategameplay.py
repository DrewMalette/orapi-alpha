import pygame

from .mob import *

class State_Create_Character:

	def __init__(self, game):
	
		self.game = game

class State_Gameplay:

	def __init__(self, game):
	
		self.game = game
		
		self.sub_state = "in_play" #None
		self.sub_states = { "fade_in": self.fade_in,
							"fade_out": self.fade_out,
							"in_play": self.in_play,
							"menu": self.menu,
							"iteming": self.iteming,
							"in_dialogue": self.in_dialogue,
							"switching": self.switching }
		
		self.input_focus = None # self.game.player
	
	def start(self):
		
		self.in_play = False
		self.ending = False
		
		self.game.terrain_renderer.update()	
				
		#debug; also needs to be put into Cutscene
		#self.engine.scene_painter.scene.sprites["2"].image.set_alpha(0)
		
		self.sub_state = "fade_in"		
		self.game.fader.fade_in()
	
	def fade_in(self): # enter?
	
		self.game.fader.update()
		self.game.terrain_renderer.render()
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_in: self.sub_state = "in_play"
		
	def fade_out(self): # exit?
	
		self.game.fader.update()
		self.game.terrain_renderer.render()
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_out:
			self.game.title_music.fadeout(800)
			self.game.switch_state("title")

	def menu(self): pass	
	def iteming(self): pass # WTF???	
	def in_dialogue(self): pass
	def switching(self): pass	

	def in_play(self): self.game.scene.update()

	def update(self): self.sub_states[self.sub_state]()
