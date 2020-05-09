import operator

import pygame

y_sort = lambda mob_list: sorted(mob_list, key=operator.attrgetter('y'))

def place(mob, col, row, terrain):
		
	mob.x = col * terrain.tilesize + (terrain.tilesize - mob.w) / 2
	mob.y = row * terrain.tilesize + (terrain.tilesize - mob.h) - 4

def load_image(filename, colourkey=None):

	try:
		image = pygame.image.load(filename)
	except:
		print("failed to load image '{}' ".format(filename))
		return

	image = image.convert()
	if colourkey != None:
		if colourkey == -1:
			colourkey = image.get_at((0,0))
		image.set_colorkey(colourkey, pygame.RLEACCEL)

	return image

def load_mob_sprite(filename):

	image = pygame.image.load(filename)
	image.convert()
	image.set_colorkey((0xff,0x00,0xff), pygame.RLEACCEL)
	cell_w, cell_h = image.get_at((0, image.get_height()-1))[:2]
	rect = pygame.Rect((0,0)+image.get_at((1, image.get_height()-1))[:2])
	offsets = image.get_at((2, image.get_height()-1))[:2]
	cols = int(image.get_width() / cell_w)
	rows = int(image.get_height() / cell_h)

	cells = {}
	for row in range(rows):
		for col in range(cols):
			cells[row*cols+col] = image.subsurface((col*cell_w, row*cell_h, cell_w, cell_h))

	return { "cols": cols, "rows": rows, "cells": cells, "rect": rect, "offsets": offsets }

def load_tileset(filename, width, height, firstgid=1):

	image = load_image(filename)
	image.set_colorkey((255,0,255), pygame.RLEACCEL)
	
	gid = int(firstgid)
	textures = {}
	cols = int(image.get_width() / width)
	rows = int(image.get_height() / height)
	for row in range(rows):
		for col in range(cols):
			x = col * width
			y = row * height
			textures[str(gid)] = image.subsurface((x, y, width, height))
			gid += 1
	
	return textures
