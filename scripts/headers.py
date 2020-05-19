# headers.py

import pygame
import api.graphics

def dialogue_init(game, text_list):

	game.obj_stack = []
	game.obj_stack.append(game.terrain_renderer)
	game.obj_stack.append(game.ui["dialoguebox"])
	
	game.ui["dialoguebox"].text_list = text_list
	game.ui["dialoguebox"].start()
	game.segment = dialogue_loop
	
def dialogue_loop(game):

	#game.scene.update()
	game.ui["dialoguebox"].update()
	
def menu_init(game):

	pass
	
def gameplay_loop(game):

	if game.controller.as_button: interact_init(game)
	if game.controller.xs_button: menu_init(game)

	game.scene.update()
	game.terrain_renderer.update()
