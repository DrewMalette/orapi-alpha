# entrytemplate.py

import pygame
import engine

# put segment functions here
def segment_template(scene):
	
	# controller input
	c = scene.game.controller			
	
	# update whatever elements need it
	
	# render necessary components

segments = locals() # so segment functions can be passed to a scene
# maybe I'll just make the dictionary myself, by hand

def run():

	pygame.init()
	
	globs = globals()
	for g in globs: print(g, globs[g])

	game = engine.graphics.Game()
	# define title image and ui components here
	
	# define your player
	game.player = engine.graphics.Mob(game, image, uid)
	# load up a scene; TODO need a reset function for a scene
	game.load_scene(name_the_scene, segments, mapfile, segment_string)
	# switch game state to the title card
	game.switch_state("title")
	
	# start the main game loop
	game.main()

