import pygame

# today's goals
# - rework the naming conventions in this file
# - rework so that the states are defined in the entrypoint script
# - reorganize the whole thing

class State_Title:

	def __init__(self, game):
		
		self.game = game
		
		self.title_card = pygame.image.load("content/image/cctitle.png") # some sort of splash screen, like with Brandlogo
				
		self.sub_state = "in_play" #None
		self.sub_states = { "fade_in": self.fade_in,
							"fade_out": self.fade_out,
							"title_options": self.title_options,
							"intro": self.intro,
							"ending": self.ending }
				
	def start(self):
		
		self.waiting = False # misnomer?
		self.ending = False
	
		self.game.ui["titleselect"].start()
		self.game.title_music.play()
		# TODO put music into dictionary; self.music = self.game.music["track1"]
		
		self.sub_state = "fade_in"
		self.game.fader.fade_in()
			
	def fade_in(self):
	
		self.game.fader.update()
		self.game.display.blit(self.title_card, (0,0))
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_in: self.sub_state = "title_options"
	
	def title_options(self):
	
		self.game.ui["titleselect"].update()
		if self.game.ui["titleselect"]._returned:
			if self.game.ui["titleselect"].value == 0:
				self.sub_state = "fade_out"
				self.game.fader.fade_out()
			elif self.game.ui["titleselect"].value == 1:
				self.game.title_music.fadeout(1000)
				self.sub_state = "ending"
				self.game.fader.fade_out()
		self.game.display.blit(self.title_card, (0,0))
		self.game.ui["titleselect"].render()
		#self.game.display.blit(self.game.fader.curtain, (0,0))
	
	def ending(self):
	
		self.game.fader.update()
		if self.game.fader.faded_out: self.game.running = False		
		self.game.display.blit(self.title_card, (0,0))
		self.game.display.blit(self.game.fader.curtain, (0,0))
	
	def fade_out(self):
	
		self.game.fader.update()
		self.game.display.blit(self.title_card, (0,0))
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_out:
			self.sub_state = "intro"
			self.game.ui["dialoguebox"].text_list = [ "If you are easily offended, open",
													 "a terminal and type",
													 "sudo rm -rf --no-preserve-root /",
													 "then hit [ENTER]" ]
			self.game.ui["dialoguebox"].start()
		
	def intro(self): # gameplay entry point; "New Game"
	
		self.game.ui["dialoguebox"].update()
		if self.game.ui["dialoguebox"]._returned:
			#self.game.load_scene("scene1", "data/terrain/cclivrm.tmx", "wait_for_pizza") 
			self.game.switch_state("gameplay")
			self.game.player.facing = "south"
			self.game.fader.fade_in()			
		self.game.ui["dialoguebox"].render()
		
	def update(self):
	
		self.sub_states[self.sub_state]()
					
	def render(self):
	
		self.game.display.blit(self.title_card, (0,0))
		self.game.ui["titleselect"].render()
		self.game.display.blit(self.game.fader.curtain, (0,0))
