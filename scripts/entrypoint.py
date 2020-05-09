# entrypoint.py

import pygame
import api.graphics

def exposition(scene):
	
	c = scene.game.controller			
	if c.exit == 1:	scene.par_state.sub_state = "fade_out"; scene.game.fader.fade_out()
		
	scene.game.ui["dialoguebox"].update()
		
	scene.game.terrain_renderer.render()
	scene.game.ui["dialoguebox"].render()
		
def wait_for_pizza(scene):

	c = scene.game.controller		
	api.graphics.move_mob(scene.game.player, 1 * c.x_axis, 1 * c.y_axis)
	if c.exit == 1:	scene.par_state.sub_state = "fade_out"; scene.game.fader.fade_out()
	
	scene.game.terrain_renderer.update()	
	
	scene.game.terrain_renderer.render()
	scene.game.ui["dialoguebox"].render()

_locals = locals()

def run():

	pygame.init()

	game = api.graphics.Game()
	# TODO define ui components here
	game.player = api.graphics.Mob(game, "content/image/mob_jon.png", "Jon")
	game.load_scene("scene1", _locals, "content/terrain/cclivrm.tmx", "wait_for_pizza") # TODO does not reset
	game.switch_state("title")
	
	game.main()

