# entrypoint.py

import pygame
import api.graphics

def title_init(game): # inits always clear game.obj_stack

	game.obj_stack = []
	game.obj_stack.append(game.title_card)
	game.obj_stack.append(game.fader)
	game.obj_stack.append(game.ui["titleselect"])
		
	game.ui["titleselect"].start()
	game.music_tracks["titletrack"].play()		
	game.fader.fade_in()
	
	game.segment = title_loop
	
def title_loop(game):

	if game.ui["titleselect"]._returned:
		if game.ui["titleselect"].value == 0:
			game.fader.fade_out()
			game.segment = fade_next
			# game.next_function = something!
			# game.load_scene()
		elif game.ui["titleselect"].value == 1:
			game.music_tracks["titletrack"].fadeout(1000)
			game.fader.fade_out()
			game.segment = fade_quit
		game.ui["titleselect"].visible = False

def start_init(game): # think of a better word than "start"

	game.obj_stack = []
	game.obj_stack.append(game.ui["dialoguebox"])

	game.ui["dialoguebox"].text_list = [ "If you are easily offended, open",
									     "a terminal and type",
										 "sudo rm -rf --no-preserve-root /",
										 "then hit [ENTER]", " ", " ",
										 "Taking your pants off is not",
										 "required but is HIGHLY",
										 "recommended." ]
	game.ui["dialoguebox"].start()
	game.segment = start_loop

def start_loop(game):

	if game.ui["dialoguebox"]._returned:
		pygame.quit()
		exit()

def fade_next(game): # put this in game?

	if game.fader.faded_out: game.segment = start_init
	
def fade_quit(game):

	if game.fader.faded_out: pygame.quit(); exit()

def run():

	pygame.init()
	game = api.graphics.Game("content/image/cctitle.png")
	game.ui["dialoguebox"] = api.graphics.UI_Dialogue("dialoguebox", game, (170,360), (300,100))
	game.ui["titleselect"] = api.graphics.UI_Select("titleselect", game, (245,300), (150,54), ["Get Cucked", "Quit to Desktop"])
	game.music_tracks["titletrack"] = pygame.mixer.Sound("content/sound/ccsong.ogg")
	game.player = api.graphics.Mob(game, "content/image/mob_jon.png", "Jon")
	title_init(game)
	game.main()

