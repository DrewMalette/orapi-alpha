# entrytemplate.py

import pygame
import orapi

# put segment functions here
def segment_template(scene):
	
	# controller input
	c = scene.game.controller			
	
	# update whatever elements need it
	
	# render necessary components

segments = locals() # so segment functions can be passed to a scene

def run():

	pygame.init()

	game = orapi.Game("0.2")
	# define title image and ui components here
	
	# define your player
	game.player = orapi.Mob(game, image, uid)
	# load up a scene; TODO need a reset function for a scene
	game.load_scene(name_the_scene, segments, mapfile, segment_string)
	# switch game state to the title card
	game.switch_state("title")
	
	# start the main game loop
	game.main()

