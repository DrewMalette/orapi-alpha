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

def title_init(game):
		
	game.ui["titleselect"].start()
	game.music_tracks["titletrack"].play()
		
	game.fader.fade_in()
	game.segment = title_loop
	
def title_loop(game):

	game.fader.update()
	game.ui["titleselect"].update()
	if game.ui["titleselect"]._returned:
		if game.ui["titleselect"].value == 0:
			game.fader.fade_out()
			game.segment = fading
			# game.next_function = something!
		elif game.ui["titleselect"].value == 1:
			game.music_tracks["titletrack"].fadeout(1000)
			game.fader.fade_out()
			game.segment = fading
	game.display.blit(game.title_card, (0,0))
	game.display.blit(game.fader.curtain,(0,0))
	game.ui["titleselect"].render()

def fading(game):

	game.fader.update()
	game.display.blit(game.fader.curtain,(0,0))
	if game.fader.faded_in or game.fader.faded_out:
		print("We're done here")
		pygame.quit()
		exit()

_locals = locals()

def run():

	pygame.init()

	game = api.graphics.Game("content/image/cctitle.png")
	# TODO define ui components here
	game.ui["dialoguebox"] = api.graphics.UI_Dialogue("dialoguebox", game, (170,360), (300,100))
	game.ui["titleselect"] = api.graphics.UI_Select("titleselect", game, (245,300), (150,54), ["Get Cucked", "Quit to Desktop"])
	game.music_tracks["titletrack"] = pygame.mixer.Sound("content/sound/ccsong.ogg")
	game.player = api.graphics.Mob(game, "content/image/mob_jon.png", "Jon")
	#game.load_scene("scene1", _locals, "content/terrain/cclivrm.tmx", "wait_for_pizza") # TODO does not reset
	#game.switch_state("title")
	game.segment = title_init
	
	game.main()

