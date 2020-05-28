# entrypoint.py

import os

import pygame
import api.graphics
	
def newgame_init(game):

	game.load_scene("scene1", os.path.join("content", "terrain", "cclivrm.tmx"))
	
	game.obj_stack = []
	game.obj_stack.append(game.scene)
	game.obj_stack.append(game.fader)
	
	game.renderer.following = game.player
	
	game.fader.fade_in()
	
	game.script = newgame_loop # eventually, newgame will not have a loop
	
def newgame_loop(game):

	game.player.move(game.controller.x_axis, game.controller.y_axis)
	
	if game.controller.exit: pygame.quit(); exit()	

def title_init(game): # inits always clear game.obj_stack

	game.obj_stack = []
	game.obj_stack.append(game.title_card)
	game.obj_stack.append(game.fader)
	game.obj_stack.append(game.ui["titleselect"])
		
	game.ui["titleselect"].start()
	game.fader.fade_in()
	
	game.script = title_loop
	
def title_loop(game):

	if game.ui["titleselect"]._returned:
		if game.ui["titleselect"].value == 0:
			game.fader.fade_out()
			game.script = fade_next
			# game.next_function = something!
			# game.load_scene()
		elif game.ui["titleselect"].value == 1:
			game.music_tracks["titletrack"].fadeout(1000)
			game.fader.fade_out()
			game.script = fade_quit
		game.ui["titleselect"].visible = False

def fade_next(game): # put this in game?

	if game.fader.faded_out: newgame_init(game)
	
def fade_quit(game):

	if game.fader.faded_out: pygame.quit(); exit()

# TODO new convention???
def fadeout(game, next_script, speed=8):

	game.next_script = next_script
	game.fader.fade_out(speed)
	game.script = fadeout_loop
	
def fadeout_loop(game):

	if fader.faded_out: game.script = game.next_script

def run():

	pygame.init()
	game = api.graphics.Game(os.path.join("content", "image", "cctitle.png"))
	game.ui["dialoguebox"] = api.graphics.UI_Dialogue("dialoguebox", game, (170,360), (300,100))
	game.ui["titleselect"] = api.graphics.UI_Select("titleselect", game, (245,300), (150,54), ["New Game", "Quit to Desktop"])
	game.player = api.graphics.Mob(game, os.path.join("content", "image", "jontest.png"), "Jon")
	title_init(game)
	game.main()

