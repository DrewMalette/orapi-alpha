# entrypoint.py

import os

import pygame
import engine.core
from engine.core import filepaths
	
def newgame_init(game):

	game.load_scene("scene1", os.path.join(filepaths.scene_path, "cclivrm.tmx"))
	
	game.obj_stack = []
	game.obj_stack.append(game.scene)
	game.obj_stack.append(game.fader)
	
	game.renderer.following = game.player
	
	game.next_script = newgame_loop # eventually newgame will not have a loop
	game.fader.fade_in()
	
def newgame_loop(game):

	game.player.move(game.controller.x_axis, game.controller.y_axis)
	
	if game.controller.exit: pygame.quit(); exit()

def title_init(game): # inits always clear game.obj_stack

	game.obj_stack = []
	game.obj_stack.append(game.title_card)
	game.obj_stack.append(game.fader)
	game.obj_stack.append(game.ui["titleselect"])
		
	game.ui["titleselect"].start()
	
	game.next_script = title_loop
	game.fader.fade_in()
	
def title_loop(game):

	if game.ui["titleselect"]._returned:
		if game.ui["titleselect"].value == 0: # New Game
			game.next_script = newgame_init
			game.fader.fade_out()			
		elif game.ui["titleselect"].value == 1: # Quit to Desktop
			#game.music_tracks["titletrack"].fadeout(1000)
			game.next_script = game.exit
			game.fader.fade_out()
		game.ui["titleselect"].visible = False

def run():

	pygame.init()
	game = engine.core.Game(os.path.join(filepaths.image_path, "cctitle.png"))
	game.ui["dialoguebox"] = engine.core.UI_Dialogue("dialoguebox", game, (170,360), (300,100))
	game.ui["titleselect"] = engine.core.UI_Select("titleselect", game, (245,300), (150,54), ["New Game", "Quit to Desktop"])
	game.player = engine.core.Mob(game, os.path.join(filepaths.image_path, "jontest.png"), "Jon")
	title_init(game)
	game.main()

