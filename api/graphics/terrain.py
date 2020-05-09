import xml.etree.ElementTree as ET

import pygame

from . import mob
from . import utilities

class Tileset:

	def __init__(self, width, height):
	
		self.width = height
		self.height = height
					
		self.textures = {}
		
	def update(self, filename, firstgid=1):
	
		textures = utilities.load_tileset("content/terrain/"+filename, self.width, self.height, firstgid)
		self.textures.update(textures)
				
	def __getitem__(self, key=-1):
	
		if key is -1:
			return self.textures
		if key is not -1:
			return self.textures[key]
			
class Terrain:

	def __init__(self, filename, engine, scene):

		self.uid = filename
		self.scene = scene
		self.scene.terrain = self
		
		tree = ET.parse(self.uid)
		root = tree.getroot()
		
		self.cols = int(root.attrib["width"])
		self.rows = int(root.attrib["height"])
		
		self.tilewidth = int(root.attrib["tilewidth"])
		self.tileheight = int(root.attrib["tileheight"])
		self.tilesize = self.tilewidth # assumes a square tile
		
		self.tileset = Tileset(self.tilewidth, self.tileheight)
		
		self.loot = {}
		self.loot_count = 0
		
		self.layerdata = { "bottom": None,
				           "middle": None,
					  	   "top": None,
					  	   "collide": None
						 }

		self.switches = {}
		
		for tilesettag in root.iter("tileset"):
			filename = tilesettag.attrib["source"]
			tilestree = ET.parse("content/terrain/"+filename)
			tilesroot = tilestree.getroot()
			for tileset in tilesroot.iter("tileset"):
				for i in tileset.iter("image"):
					filename = i.attrib["source"]
					firstgid = tilesettag.attrib["firstgid"]
					self.tileset.update(filename, firstgid) # ummmmmmm....?
					
		for layer in root.iter("layer"):
			for data in layer.iter("data"):
				name = layer.attrib['name']
				rawdata = data.text.split(",")
				cleandata = []
				for tile in rawdata:
					cleandata.append(tile.strip())
				self.layerdata[name] = cleandata
				
		for layer in root.iter("objectgroup"):
			for rect in layer.iter("object"):
				rectattribs = {}
				for v in rect.attrib.keys():
					rectattribs[v] = rect.attrib[v]
				for proptag in rect.iter("properties"):
					for propchild in proptag.iter("property"):
						index = propchild.attrib["name"]
						value = propchild.attrib["value"]
						rectattribs[index] = value
				
				uid = rectattribs["id"]
				col = int(float(rectattribs["x"]) / self.tilewidth)
				row = int(float(rectattribs["y"]) / self.tileheight)
				if rectattribs["type"] == "player":
					if engine.player is None: # move this to engine
						print("player object is not defined")
						print("exiting")
						pygame.quit()
						exit()
					self.scene.live_mobs["player"] = engine.player
					self.scene.live_mobs["player"].scene = self.scene
					utilities.place(self.scene.live_mobs["player"], col, row, self)
				elif rectattribs["type"] == "switch":
					x = int(float(rectattribs["x"]) / self.tilewidth) * self.tilewidth
					y = int(float(rectattribs["y"]) / self.tileheight) * self.tileheight
					facing = rectattribs["facing"]
					try:
						c = int(rectattribs["col"])
						r = int(rectattribs["row"])
						self.switches[uid] = [pygame.Rect((x,y,self.tilewidth,self.tileheight)), rectattribs["Filename"], (c,r), facing]
					except:
						#print("defaulting to map defined placement position")
						self.switches[uid] = [pygame.Rect((x,y,self.tilewidth,self.tileheight)), rectattribs["Filename"], None, facing]
				elif rectattribs["type"] == "mob":
					self.scene.live_mobs[uid] = mob.Mob("content/image/" + rectattribs["Filename"], rectattribs["name"])
					self.scene.live_mobs[uid].scene = self.scene
					utilities.place(self.scene.live_mobs[uid], col, row, self)
				#elif rectattribs["type"] == "static":
				#	filepath = "content/image/" + rectattribs["Filename"]
				#	name = rectattribs["name"]
				#	self.sprites[uid] = sprite.Static(filepath, name)
				#	self.sprites[uid].scene = self
				#	self.sprites[uid].place(col,row)

	def get_tile(self, layername, col, row):
	
		index = int((row % self.rows) * self.cols + (col % self.cols))
		return self.layerdata[layername][index]
		
	def add_loot(self, filename, x, y):
	
		uid = self.loot_count
		px = x
		py = y - 20
		self.loot[self.loot_count] = sprite.Loot(self, uid, filename, (px,py))
		self.loot_count = (self.loot_count + 1) % 256
